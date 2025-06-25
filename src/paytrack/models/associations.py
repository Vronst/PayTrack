from sqlalchemy import Table, Column, ForeignKey
from . import Base


association_included = Table(
        "association_included",
        Base.metadata,
        Column("user_id", ForeignKey("users.id"), primary_key=True),
        Column("included_user_id", ForeignKey("users.id"), primary_key=True)
)

association_transaction = Table(
        'association_transaction',
        Base.metadata,
        Column('user_id', ForeignKey('users.id'), primary_key=True),
        Column('included_to_transaction', ForeignKey('transactions.id'), primary_key=True)
)

association_receivers = Table(
        'association_receivers',
        Base.metadata,
        Column('user_id', ForeignKey('users.id'), primary_key=True),
        Column('receiver_shared_with', ForeignKey('receivers.id'), primary_key=True)
)
