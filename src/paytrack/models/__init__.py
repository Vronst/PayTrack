from sqlalchemy.orm import configure_mappers
from .base import Base
from .user import User
from .setting import Setting
from .language import Language
from .transaction import Transaction
from .receiver import Receiver
from .category import Category
from .currency import Currency
from .savings import Savings
from .subscription_share import SubscriptionShare 
from .transaction_share import TransactionShare 
from .translation import Translation
from .subscription import Subscription


configure_mappers()
