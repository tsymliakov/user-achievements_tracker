from fastapi import APIRouter
from fastapi_pagination import add_pagination, Page
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi_pagination.ext.sqlalchemy import paginate
from src.database import session_maker, session_old_maker
from src.models import *


from pydantic import BaseModel


class PydanticUser(BaseModel):
    id: int
    name: str
    language: str


class PydanticAchievment(BaseModel):
    id: int
    name_ru: str
    name_en: str
    points: int
    ru_description: str
    en_description: str


users_router = APIRouter(
    prefix="/users",
    tags=["Пользователи"],
    responses={404: {"description": "Not found"}},
)


achievment_router = APIRouter(
    prefix="/achievments",
    tags=["Достижения"],
    responses={404: {"description": "Not found"}},
)


@users_router.get("/")
def get_all_users() -> Page[PydanticUser]:
    with session_maker() as session:
        stmt = select(User)
    return paginate(session, stmt)


@users_router.get("/{id}")
def get_user(id: int):
    with session_maker() as session:
        user = session.get(User, id) or "User not found"
    return user

add_pagination(users_router)


@achievment_router.get("/")
def get_achievments() -> Page[PydanticAchievment]:
    stmt = select(Achievment)

    with session_maker() as session:
        return paginate(session, stmt)


add_pagination(achievment_router)
