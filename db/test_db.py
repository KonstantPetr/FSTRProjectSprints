import os
from dotenv import load_dotenv, find_dotenv

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import NullPool


load_dotenv(find_dotenv())

TEST_DB_HOST = os.environ.get('TEST_DB_HOST')
TEST_DB_PORT = os.environ.get('TEST_DB_PORT')
TEST_DB_LOGIN = os.environ.get('TEST_DB_LOGIN')
TEST_DB_PASS = os.environ.get('TEST_DB_PASS')
TEST_DB_NAME = os.environ.get('TEST_DB_NAME')

SQLALCHEMY_DATABASE_URL = f'postgresql://{TEST_DB_LOGIN}:{TEST_DB_PASS}@{TEST_DB_HOST}:{TEST_DB_PORT}/{TEST_DB_NAME}'

engine = create_engine(SQLALCHEMY_DATABASE_URL, poolclass=NullPool)

Base = declarative_base()
