"""
Модели для валидации данных.
"""
from datetime import date
from pydantic import BaseModel, \
                     EmailStr, \
                     Field


class UserIn(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    surname: str | None = Field(None, min_length=2, max_length=50)
    email: EmailStr = Field(..., max_length=128)
    password: str = Field(..., min_length=6, max_length=50)


class UserOut(BaseModel):
    id: int = Field(...)
    name: str = Field(..., min_length=2, max_length=50)
    surname: str | None = Field(None, min_length=2, max_length=50)
    email: EmailStr = Field(..., max_length=128)
    password: str = Field(..., min_length=6, max_length=50)


class ProductIn(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    description: str | None = Field(None, min_length=2, max_length=50)
    price: int = Field(...)


class ProductOut(BaseModel):
    id: int = Field(...)
    name: str = Field(..., min_length=2, max_length=50)
    description: str | None = Field(None, min_length=2, max_length=50)
    price: int = Field(...)


class OrdersInForCreate(BaseModel):
    user_id: int = Field(...)
    product_id: int = Field(...)


class OrdersInForUpdate(BaseModel):
    status_order: bool = Field(...)


class OrdersOut(BaseModel):
    id: int = Field(...)
    user_id: int = Field(...)
    product_id: int = Field(...)
    order_date: date = Field(...)
    status_order: bool = Field(...)
