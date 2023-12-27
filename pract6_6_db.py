"""
Модели для базы данных .
"""
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import CheckConstraint, ForeignKey, Boolean, Integer, Column, String, Date


Base = declarative_base()


class User(Base):

    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), CheckConstraint('LENGTH(name) >= 2'), nullable=False)
    surname = Column(String(50), CheckConstraint('LENGTH(surname) >= 2'))
    email = Column(String(128), unique=True, nullable=False)
    password = Column(String(50), CheckConstraint('LENGTH(password) >= 6'), nullable=False)
    information_about_orders = relationship("Orders", backref="user", cascade="all, delete")


class Products(Base):

    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), CheckConstraint('LENGTH(name) >= 2'), nullable=False)
    description = Column(String(50), CheckConstraint('LENGTH(description) >= 2'))
    price = Column(Integer, nullable=False)
    information_about_orders = relationship("Orders", backref="products")


class Orders(Base):

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    order_date = Column(Date, nullable=False)
    status_order = Column(Boolean, nullable=False)
