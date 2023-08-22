from fastapi import APIRouter, Depends, HTTPException

from fastapi_users import FastAPIUsers
from database import User
from auth.manager import get_user_manager
from auth.auth_config import auth_backend

from models import models
from schemas import schemas

from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session

from fastapi.encoders import jsonable_encoder

book_router = APIRouter(
    prefix='/book',
    tags=['Book']
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()


@book_router.get("/")
async def get_all_books(session: AsyncSession = Depends(get_async_session)):
    query = select(models.book).limit(10)
    result = await session.execute(query)
    return result.all()


@book_router.post("/add/")
async def add_book(new_book: schemas.SchemaBook,
                   session: AsyncSession = Depends(get_async_session),
                   user: User = Depends(current_user)):
    smtp = insert(models.book).values(**new_book.dict())
    await session.execute(smtp)
    await session.commit()
    return {"message": "Book created"}


@book_router.delete("/delete/")
async def del_book(book_id: int, session: AsyncSession = Depends(get_async_session),
                   user: User = Depends(current_user)):
    smtp = delete(models.book).where(models.book.c.id == book_id)
    await session.execute(smtp)
    await session.commit()
    return {"message": "Book has been deleted"}


