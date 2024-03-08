from sqlalchemy import create_engine
from dotenv import dotenv_values

from sqlalchemy.orm import declarative_base



class Engine:
    
    config = dotenv_values('.env')
    
    db_user = config['db_user']
    db_password = config['db_password']
    db_host = config['db_host']
    db_port = config['db_port']
    db_name = config['db_name']
    
    connection_string = f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    # connection_string = 'postgresql+psycopg2://airflow:airflow@postgresql:5432/airflow'
    engine = None
    
    @classmethod
    def create_or_get_engine(cls):
        # if cls.engine == None:
        #     cls.engine = create_engine(cls.connection_string)
        return create_engine(cls.connection_string)

    
    

    

