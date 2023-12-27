"""
#### Задание №6
- Необходимо создать базу данных для интернет-магазина. База данных должна
состоять из трех таблиц: товары, заказы и пользователи. Таблица товары должна
содержать информацию о доступных товарах, их описаниях и ценах. Таблица
пользователи должна содержать информацию о зарегистрированных
пользователях магазина. Таблица заказы должна содержать информацию о
заказах, сделанных пользователями.
○ Таблица пользователей должна содержать следующие поля: id (PRIMARY KEY),
имя, фамилия, адрес электронной почты и пароль.
○ Таблица товаров должна содержать следующие поля: id (PRIMARY KEY),
название, описание и цена.
○ Таблица заказов должна содержать следующие поля: id (PRIMARY KEY), id
пользователя (FOREIGN KEY), id товара (FOREIGN KEY), дата заказа и статус
заказа.
- Создайте модели pydantic для получения новых данных и
возврата существующих в БД для каждой из трёх таблиц
(итого шесть моделей).
- Реализуйте CRUD операции для каждой из таблиц через
создание маршрутов, REST API (итого 15 маршрутов).
○ Чтение всех
○ Чтение одного
○ Запись
○ Изменение
○ Удаление
"""
import databases
from typing import List
from datetime import date
from fastapi import FastAPI, Path
from sqlalchemy import create_engine
from starlette.responses import JSONResponse
from sqlalchemy.sql import insert, select, update, delete
from pract6_6_db import Base, User, Products, Orders
from pract6_6_validation import UserIn, \
                                                UserOut, \
                                                OrdersOut, \
                                                ProductIn, \
                                                ProductOut, \
                                                OrdersInForCreate, \
                                                OrdersInForUpdate

DATABASE_URL = "sqlite:///database_pract6_6.db"

database = databases.Database(DATABASE_URL)

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/users/", response_model=UserOut)
async def create_one_user(user: UserIn):

    new_user = \
        insert(User).values(name=user.name,
                            surname=user.surname,
                            email=user.email,
                            password=user.password)
    await database.execute(new_user)

    query_sql = \
        select(User).where(User.email == user.email)

    answer_for_id_user = \
        await database.fetch_one(query_sql)

    answer = \
        {"id": answer_for_id_user[0], **user.dict()}

    return JSONResponse(content=answer, status_code=200)


@app.get("/users/{user_id}", response_model=UserOut | None)
async def read_user(user_id: int = Path(..., ge=1)):

    query_sql = \
        select(User).where(User.id == user_id)

    answer = await database.fetch_one(query_sql)

    if answer:

        return {
            "id": answer[0],
            "name": answer[1],
            "surname": answer[2],
            "email": answer[3],
            "password": answer[4],
        }


@app.get("/users/", response_model=List[UserOut])
async def read_all_users():

    sql_query = select(User)

    all_user = await database.fetch_all(sql_query)

    tasks: list = []

    for one_user in all_user:
        tasks.append({
            "id": one_user[0],
            "name": one_user[1],
            "surname": one_user[2],
            "email": one_user[3],
            "password": one_user[4],
        })

    return JSONResponse(content=tasks, status_code=200)


@app.put("/users/{user_id}", response_model=UserOut | None)
async def update_user(update_user: UserIn, user_id: int = Path(..., ge=1)):

    query = \
        update(User).where(User.id == user_id).values(**update_user.dict())

    if await database.execute(query):
        return {
            "id": user_id,
            "name": update_user.name,
            "surname": update_user.surname,
            "email": update_user.email,
            "password": update_user.password
        }


@app.delete("/users/{user_id}")
async def delete_user(user_id: int = Path(..., ge=1)):

    query_sql = \
        delete(User).where(User.id == user_id)

    if await database.execute(query_sql):
        return {'delete user': user_id}


@app.post("/products/", response_model=ProductOut)
async def create_one_product(product: ProductIn):

    new_product = \
        insert(Products).values(name=product.name,
                                description=product.description,
                                price=product.price)
    await database.execute(new_product)

    query_sql = \
        select(Products).where(Products.name == product.name,
                               Products.description == product.description,
                               Products.price == product.price)

    answer_for_id_product = \
        await database.fetch_one(query_sql)

    answer = \
        {"id": answer_for_id_product[0], **product.dict()}

    return JSONResponse(content=answer, status_code=200)


@app.get("/products/{product_id}", response_model=ProductIn | None)
async def read_product(product_id: int = Path(..., ge=1)):

    query_sql = \
        select(Products).where(Products.id == product_id)

    answer = await database.fetch_one(query_sql)

    if answer:

        return {
            "id": answer[0],
            "name": answer[1],
            "description": answer[2],
            "price": answer[3]
        }


@app.get("/products/", response_model=List[ProductOut])
async def read_all_products():

    sql_query = select(Products)

    all_products = await database.fetch_all(sql_query)

    products: list = []

    for one_product in all_products:
        products.append({
            "id": one_product[0],
            "name": one_product[1],
            "description": one_product[2],
            "price": one_product[3]
        })

    return JSONResponse(content=products, status_code=200)


@app.put("/products/{product_id}", response_model=ProductOut | None)
async def update_product(update_product: ProductIn, product_id: int = Path(..., ge=1)):

    query_sql = \
        update(Products).where(Products.id ==
                               product_id).values(**update_product.dict())

    if await database.execute(query_sql):
        return {
            "id": product_id,
            "name": update_product.name,
            "description": update_product.description,
            "price": update_product.price,
        }


@app.delete("/products/{product_id}")
async def delete_product(product_id: int = Path(..., ge=1)):

    query_sql = \
        delete(Products).where(Products.id == product_id)

    if await database.execute(query_sql):
        return {'delete product': product_id}


@app.post("/orders/", response_model=OrdersOut | None)
async def create_one_order(order: OrdersInForCreate):

    check_user_query = \
        select(User).where(User.id == order.user_id)

    check_product_query = \
        select(Products).where(Products.id == order.product_id)

    if await database.fetch_one(check_user_query) and \
            await database.fetch_one(check_product_query):

        new_order = \
            insert(Orders).values(user_id=order.user_id,
                                  product_id=order.product_id,
                                  order_date=date.today(),
                                  status_order=False)

        if await database.execute(new_order):

            answer_for_id_order = await database.fetch_one(
                select(Orders).where(Orders.user_id == order.user_id).order_by(Orders.id.desc())
            )

            answer = \
                {
                    "id": answer_for_id_order[0],
                    "user_id": answer_for_id_order[1],
                    "product_id": answer_for_id_order[2],
                    "order_date": str(answer_for_id_order[3]),
                    "status_order": answer_for_id_order[4]
                }

            return JSONResponse(content=answer, status_code=200)


@app.get("/orders/{order_id}", response_model=OrdersOut | None)
async def read_order(order_id: int = Path(..., ge=1)):

    query_sql = \
        select(Orders).where(Orders.id == order_id)

    answer = await database.fetch_one(query_sql)

    if answer:

        return {
            "id": answer[0],
            "user_id": answer[1],
            "product_id": answer[2],
            "order_date": str(answer[3]),
            "status_order": answer[4]
        }


@app.get("/orders/", response_model=List[OrdersOut])
async def read_all_orders():

    sql_query = select(Orders)

    all_orders = \
        await database.fetch_all(sql_query)

    orders: list = []

    for one_order in all_orders:
        orders.append({
            "id": one_order[0],
            "user_id": one_order[1],
            "product_id": one_order[2],
            "order_date": str(one_order[3]),
            "status_order": one_order[4]
        })

    return JSONResponse(content=orders, status_code=200)


@app.put("/orders/{order_id}", response_model=OrdersOut | None)
async def update_order(update_order: OrdersInForUpdate, order_id: int = Path(..., ge=1)):

    query_sql = \
        update(Orders).where(Orders.id ==
                             order_id).values(**update_order.dict())

    if await database.execute(query_sql):

        query_sql = \
            select(Orders).where(Orders.id == order_id)

        answer = \
            await database.fetch_one(query_sql)

        if answer:

            return {
                "id": answer[0],
                "user_id": answer[1],
                "product_id": answer[2],
                "order_date": str(answer[3]),
                "status_order": answer[4]
            }


@app.delete("/orders/{orders_id}")
async def delete_order(orders_id: int = Path(..., ge=1)):

    query_sql = \
        delete(Orders).where(Orders.id == orders_id)

    if await database.execute(query_sql):
        return {'delete product': orders_id}


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
