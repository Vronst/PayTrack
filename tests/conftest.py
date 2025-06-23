import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from paytrack.models import Base


@pytest.fixture(scope='function')
def session():
    engine = create_engine('sqlite:///:memory:', echo=True)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()

