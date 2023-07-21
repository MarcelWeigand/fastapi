from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings


#SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Bayernamas1900?@localhost/fastapi'
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

print(SQLALCHEMY_DATABASE_URL)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# dependency
def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()


# while True:
#     try:
#         conn = psycopg2.connect(host = 'localhost',
#                                 database = 'fastapi', #database name in postgres
#                                 user = 'postgres', #default postgres username
#                                 password = 'Bayernamas1900?',
#                                 cursor_factory=RealDictCursor #give column names as well
#                                 )
#         cursor = conn.cursor()
#         print("DB connection suc")
#         break
#     except Exception as error:
#         print("Connection failed")
#         print("Error: ", error)
#         time.sleep(2)