import os
from dotenv import load_dotenv, find_dotenv

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from db.schemas import Users, Coords, Levels, Images, PerevalAdded


load_dotenv(find_dotenv())

FSTR_DB_HOST = os.environ.get('FSTR_DB_HOST')
FSTR_DB_PORT = os.environ.get('FSTR_DB_PORT')
FSTR_DB_LOGIN = os.environ.get('FSTR_DB_LOGIN')
FSTR_DB_PASS = os.environ.get('FSTR_DB_PASS')
FSTR_DB_NAME = os.environ.get('FSTR_DB_NAME')

SQLALCHEMY_DATABASE_URL = f'postgresql://{FSTR_DB_LOGIN}:{FSTR_DB_PASS}@{FSTR_DB_HOST}:{FSTR_DB_PORT}/{FSTR_DB_NAME}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
