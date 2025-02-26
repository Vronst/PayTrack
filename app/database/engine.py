import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, scoped_session
from ..service import simple_logs


load_dotenv()

class MyEngine:

    def __init__(self, test: bool = False, test_db: str = ''):
        self.test = test
        self.POSTGRES_USER = os.getenv('POSTGRES_USER', None)
        self.POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', None)
        self.POSTGRES_HOST = os.getenv('POSTGRES_HOST', None)
        self.POSTGRES_PORT = os.getenv('POSTGRES_PORT', None)
        if self.test:
            self.POSTGRES_DB = test_db
        else:
            self.POSTGRES_DB = os.getenv('POSTGRES_DB', None)

        if not all([
            self.POSTGRES_USER,
            self.POSTGRES_PASSWORD, 
            self.POSTGRES_HOST,
            self.POSTGRES_DB,
            self.POSTGRES_PORT]):
            raise ValueError('One or more environment variables are not set')

    def create_my_session(self) -> scoped_session:
        if not self.POSTGRES_DB:
            raise ValueError('Missing env variable - POSTGRESS_DB')
        self.engine: Engine = create_engine(
            f'postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}'
                f'@{self.POSTGRES_HOST}:{self.POSTGRES_PORT or 5432}/{self.POSTGRES_DB}')
        local_session: sessionmaker = sessionmaker(bind=self.engine)
        self.session: scoped_session = scoped_session(local_session)

        with self.engine.begin() as conn:
            from .models import Base
            Base.metadata.create_all(bind=conn)
        from ..utils import simple_logs
        simple_logs('Tables created successfully', log_file=['logs.txt', 'db.log'])

        return self.session
    
    def close_session(self):
        if self.test:
            with self.engine.begin() as conn:
                from.models import Base
                Base.metadata.drop_all(conn)
                simple_logs('Tables dropped successfully', log_file=['logs.txt', 'db.log'])
        self.session.remove()
        simple_logs('Session removed successfully', log_file=['logs.txt', 'db.log'])
