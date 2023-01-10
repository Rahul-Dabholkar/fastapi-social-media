from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#-----------------| ESTABLISING CONNECTION TO DATABASE VIA psycopg2 |----------------------
'''
import psycopg2
from psycopg2.extras import RealDictCursor # for column names
import time

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapiDB', user='postgres', password='7421', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database Connection was successfull')
        break
    except Exception as error:
        print('Connection to database failed')
        print('Error : ', error)
        time.sleep(2)

'''