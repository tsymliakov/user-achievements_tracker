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


class Pydantic_Ach_With_Translation(BaseModel):
    name: str
    description: str


class Pydanticachievement(BaseModel):
    id: int
    points: int
    ru_achievement: Pydantic_Ach_With_Translation
    en_achievement: Pydantic_Ach_With_Translation


users_router = APIRouter(
    prefix="/users",
    tags=["Пользователи"],
    responses={404: {"description": "Not found"}},
)


achievement_router = APIRouter(
    prefix="/achievements",
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


@users_router.post("/{user_id}/add_achievement/{achievement_id}")
def add_achievement_to_user(user_id: int,
                            achievement_id: int,
                            utc_datetime: datetime = datetime.utcnow()):

    with session_factory() as session:
        user_achievement = Userachievement(user_id=user_id,
                                         achievement_id=achievement_id,
                                         awarding_datetime=utc_datetime)

        session.add(user_achievement)
        session.commit()

# todo: refactor --------------------------------------

class achievementOut(BaseModel):
    id: int
    description: str

class UserOut(BaseModel):
    id: int
    user_achievements: List[achievementOut]


@users_router.get("/{id}/achievements")
def get_user_achievements(id: int) -> UserOut:
    with session_factory() as session:
        user = session.get(User, id)

        user_lang = user.language
        print(user_lang)

        for ach in user.user_achievements:
            user_lang_achievement = getattr(ach, f"{user_lang}_achievement")
            ach.description = user_lang_achievement.description
        return user

add_pagination(users_router)


@achievement_router.get("/")
def get_all_achievements() -> Page[Pydanticachievement]:
    stmt = select(Achievement)

    with session_factory() as session:
        return paginate(session, stmt)


@achievement_router.post("/")
def create_new_achievement(points: int,
                          name_ru: str,
                          name_en: str,
                          ru_description: str,
                          en_description: str):

    new_achievement = Achievement(points,
                                name_ru,
                                name_en,
                                ru_description,
                                en_description)

    with session_factory() as session:
        session.add(new_achievement)
        session.commit()


add_pagination(achievement_router)
