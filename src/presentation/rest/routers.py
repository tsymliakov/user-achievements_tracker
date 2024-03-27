from fastapi import APIRouter
from fastapi_pagination import add_pagination, Page
from sqlalchemy import select
from fastapi_pagination.ext.sqlalchemy import paginate
from src.database import Session
from src.models import *


from pydantic import BaseModel


class PydanticUser(BaseModel):
    id: int
    name: str
    language: str


users_router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


achievment_router = APIRouter(
    prefix="/achievments",
    tags=["achievments"],
    responses={404: {"description": "Not found"}},
)


@users_router.get("/")
def get_users() -> Page[PydanticUser]:
    a = select(User)

    with Session() as session:
        return paginate(session, a)


@users_router.post("/{id}")
def add_new_user(id: int):
    with Session() as session:
        user = session.get(User, id) or "User not found"
    return user

add_pagination(users_router)
