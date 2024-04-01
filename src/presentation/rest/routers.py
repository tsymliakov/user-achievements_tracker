from fastapi import APIRouter
from datetime import datetime
from fastapi_pagination import add_pagination, Page
from sqlalchemy import insert, select
from sqlalchemy.orm import selectinload
from fastapi_pagination.ext.sqlalchemy import paginate
from src.database import session_factory
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
    with session_factory() as session:
        stmt = select(User)
    return paginate(session, stmt)


@users_router.get("/{id}")
def get_user(id: int):
    with session_factory() as session:
        user = session.get(User, id) or "User not found"
    return user


@users_router.post("/{id}")
def get_user(id: int,
             achievment_id: int,
             utc_datetime: datetime = datetime.utcnow()):

    with session_factory() as session:
        user_achievment = UserAchievment(user_id=id,
                                         achievment_id=achievment_id,
                                         awarding_datetime=utc_datetime)

        session.add(user_achievment)
        session.commit()

# todo: refactor --------------------------------------

class AchievmentOut(BaseModel):
    id: int
    description: str

class UserOut(BaseModel):
    id: int

    user_achievments: List[AchievmentOut]


@users_router.get("/{id}/achievments")
def get_user_achievments(id: int) -> UserOut:
    with session_factory() as session:
        stmt = select(User).options(selectinload(User.user_achievments)).where(User.id == id)

        user = session.execute(stmt).first()[0]
        user_achiv = user.user_achievments

        # todo:
        # monkeypatching- то работает, но вот что произойдет, если языков станет больше двух...
        # наиболее красивое решение, которое мне видется, заключается в следующем:
        # в модели Achievments стоит оставить лишь id и points, а все описания разнести по разным таблицам
        # так, чтобы на каждый язык была своя таблица описаний достижений, связать это дело через один-ко-многим.
        #
        # Таким образом после получения экземпляра модели пользователя на основании значения поля language
        # станет возможноым автоматически и почти не приходя в сознание запросить описание ачивмента из таблицы с
        # требуемым языком.
        for achievment in user_achiv:
            achievment.__dict__['description'] = achievment.ru_description if \
                                                 user.language == 'ru' else \
                                                 achievment.en_description

        return user

add_pagination(users_router)


@achievment_router.get("/")
def get_achievments() -> Page[PydanticAchievment]:
    stmt = select(Achievment)

    with session_factory() as session:
        return paginate(session, stmt)


@achievment_router.post("/")
def create_new_achievment(points: int,
                          name_ru: str,
                          name_en: str,
                          ru_description: str,
                          en_description: str):

    new_achievment = Achievment(points,
                                name_ru,
                                name_en,
                                ru_description,
                                en_description)

    with session_factory() as session:
        session.add(new_achievment)
        session.commit()


add_pagination(achievment_router)
