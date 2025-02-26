from sqlalchemy.orm import scoped_session
from .database import session as orginal_session


session: scoped_session


def start_app() -> scoped_session:
    global session
    session = orginal_session
    return session

    
def close_app() -> bool:
    session.remove()
    return True
