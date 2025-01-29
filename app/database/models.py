from typing import Union
from sqlalchemy import Integer, String, ForeignKey, Boolean, Float
from sqlalchemy.orm import (
    relationship, 
    DeclarativeBase,
    MappedColumn,
    mapped_column,
)
from ..utils import simple_logs, taxes


class Base(DeclarativeBase):
    pass


def default_taxes(user: 'User') -> None:
    from . import session
    for tax in taxes:
        tx: Tax = Tax(taxname=tax, user_id=user.id)
        session.add(tx)
        # user.taxes.append(tx)
        session.commit()
    return


class Tax(Base):
    __tablename__ = 'taxes'
    
    id: MappedColumn[int] = mapped_column(Integer, primary_key=True)
    taxname: MappedColumn[str] = mapped_column(String, unique=True)
    payment_status: MappedColumn[bool] = mapped_column(Boolean, default=False, nullable=False)
    user_id: MappedColumn[int] = mapped_column(Integer, ForeignKey('users.id'))
    
    users = relationship("User", back_populates="taxes")
    payments = relationship("Payment", back_populates="tax")

class User(Base):
    __tablename__ = 'users'
    
    id: MappedColumn[int] = mapped_column(Integer, primary_key=True)
    name: MappedColumn[str] = mapped_column(String, unique=True)
    password: MappedColumn[str] = mapped_column(String)
    
    payments = relationship("Payment", back_populates="user", cascade='all, delete-orphan')
    taxes = relationship("Tax", back_populates="users", cascade='all, delete-orphan')
    

class Payment(Base):
    __tablename__ = 'payments'
    
    id: MappedColumn[int] = mapped_column(Integer, primary_key=True)
    price: MappedColumn[float] = mapped_column(Float)
    date: MappedColumn[str] = mapped_column(String)
    taxes_id: MappedColumn[int] = mapped_column(Integer, ForeignKey('taxes.id'))
    users_id: MappedColumn[int] = mapped_column(Integer, ForeignKey('users.id'))
    
    tax = relationship("Tax", back_populates="payments")
    user = relationship("User", back_populates="payments")

    def __str__(self) -> str:
        tax_name: str = self.tax.taxname if self.tax else 'Unknown'
        return f'{tax_name}:\n{self.id=} - {self.price=} - {self.date=}'
