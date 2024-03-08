# -*- coding: utf-8 -*-

import pandas as pd
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import dotenv_values
from utils.connect_db import Engine
from sqlalchemy.orm import Session, declarative_base
# from utils.models import Comment

from sqlalchemy import Column, Integer, String, DateTime


config = dotenv_values(".env")

Base = declarative_base()

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, autoincrement= True)
    author = Column(String)
    text= Column(String)
    published_at = Column(DateTime(timezone=True))


def process_comments(response_items):
    comments = []
    for comment in response_items:
        author = comment['snippet']['topLevelComment']['snippet']['authorDisplayName']
        comment_text = comment['snippet']['topLevelComment']['snippet']['textOriginal']
        publish_at = comment['snippet']['topLevelComment']['snippet']['publishedAt']

        comment_info = {'author': author, 
                        'text': comment_text, 'published_at': publish_at}

        comments.append(comment_info)
    print(f'Finished processing {len(comments)} comments.')
    return comments

def load_comments(comments):
    from sqlalchemy import create_engine
    
    # engine= Engine.create_or_get_engine()
    engine = create_engine('postgresql+psycopg2://airflow:airflow@localhost:5432/airflow')
    
    

    Base.metadata.create_all(engine)
    
    session=Session(engine)
    
    for comment in comments:
        session.add(Comment(author=comment['author'], text=comment['text'], published_at=comment['published_at']))
        session.commit()  
        
    session.close()      

def main():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = config['GOOGLE_API_KEY']

    youtube = build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    try:
        request = youtube.commentThreads().list(
            part="snippet, replies",
            videoId="q8q3OFFfY6c"
        )
        
        response = request.execute()
        processed = process_comments(response['items'])
        
        load_comments(processed)
        
        # print(pd.DataFrame(processed))
        

    except HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred:\n{e.content}")

if __name__ == "__main__":
    main()
