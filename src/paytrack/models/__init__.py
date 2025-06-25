from sqlalchemy.orm import configure_mappers
from .base import Base
from .user import User
from .setting import Setting
from .language import Language
from .transaction import Transaction
from .receiver import Receiver
from .category import Category
from .currency import Currency


configure_mappers()
