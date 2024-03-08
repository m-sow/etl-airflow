from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, autoincrement= True)
    author = Column(String)
    text= Column(String)
    published_at = Column(DateTime(timezone=True))
    
    
    
