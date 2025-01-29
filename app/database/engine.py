import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, scoped_session


load_dotenv()

POSTGRES_USER = os.getenv('POSTGRES_USER', None)
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', None)
POSTGRES_HOST = os.getenv('POSTGRES_HOST', None)
POSTGRES_PORT = os.getenv('POSTGRES_PORT', None)
POSTGRES_DB = os.getenv('POSTGRES_DB', None)

if not all([POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_DB]):
    raise ValueError('One or more environment variables are not set')

engine: Engine = create_engine(f'postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT or 5432}/{POSTGRES_DB}')
local_session: sessionmaker = sessionmaker(bind=engine)
session = scoped_session(local_session)

with engine.begin() as conn:
    from .models import Base
    Base.metadata.create_all(bind=conn)
from ..utils import simple_logs
simple_logs('Tables created successfully', log_file=['logs.txt', 'db.log'])