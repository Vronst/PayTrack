from .database import MyEngine
from .auth import Authorization


class TaxManager:

    def __init__(self, engine: MyEngine, auth: Authorization):
        self.auth = auth
        if self.auth.user == None:
            raise ValueError('User not logged in')
        self.engine = engine
