from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import add_pagination, Page
from sqlalchemy import desc, func, select
from fastapi_pagination.ext.sqlalchemy import paginate
from src.database import session_factory, get_session, Session
from src.models import *

from sqlalchemy.exc import IntegrityError


from datetime import datetime, timedelta


from pydantic import BaseModel


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


class PydanticUser(BaseModel):
    id: int
    name: str
    language: str


@users_router.get("/")
def get_all_users(session: Session = Depends(get_session)) -> Page[PydanticUser]:
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
                            utc_datetime: datetime = datetime.utcnow(),
                            session: Session = Depends(get_session)):

    user_achievement = UserAchievement(user_id=user_id,
                                     achievement_id=achievement_id,
                                     awarding_datetime=utc_datetime)

    try:
        session.add(user_achievement)
        session.commit()
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Пользователь или достижение с заданными id не найдены.")

# todo: refactor --------------------------------------

class achievementOut(BaseModel):
    id: int
    description: str

class UserOut(BaseModel):
    id: int
    user_achievements: List[achievementOut]


@users_router.get("/{id}/achievements")
def get_user_achievements(id: int,
                          session: Session = Depends(get_session)) -> UserOut:
    user = session.get(User, id)

    user_lang = user.language

    for ach in user.user_achievements:
        user_lang_achievement = getattr(ach, f"{user_lang}_achievement")
        ach.description = user_lang_achievement.description
    return user



@users_router.get("/users/max_achievements")
def get_user_with_max_achievements(session: Session = Depends(get_session)):
    stmt = select(UserAchievement.user_id, func.count(UserAchievement.user_id).label('ach_count')).group_by(UserAchievement.user_id).order_by(desc('ach_count'))

    result = session.execute(stmt)
    return result.scalar()


@users_router.get("/users/max_points")
def get_user_with_max_points(session: Session = Depends(get_session)):
    stmt = select(UserAchievement.user_id, func.sum(Achievement.points).label('points_sum')).join_from(UserAchievement, Achievement).group_by(UserAchievement.user_id).order_by(desc('points_sum'))

    result = session.execute(stmt)
    return result.scalar()


@users_router.get("/users/max_points_difference")
def get_users_with_max_points_difference(session: Session = Depends(get_session)):
    stmt = select(UserAchievement.user_id).join_from(UserAchievement, Achievement).group_by(UserAchievement.user_id).order_by(desc(func.sum(Achievement.points)))

    result = session.execute(stmt).all()
    max_points_sum_user_id = result[0]
    min_points_sum_user_id = result[-1]

    return {'user_id_max': max_points_sum_user_id[0],
            'user_id_min': min_points_sum_user_id[0]}


@users_router.get("/users/min_points_difference")
def get_users_with_min_points_difference(session: Session = Depends(get_session)):
    stmt = select(UserAchievement.user_id, func.sum(Achievement.points).label('points_sum')).join_from(UserAchievement, Achievement).group_by(UserAchievement.user_id)

    user_point_sums = session.execute(stmt).all()
    session.close()

    # SQLAlchemy нативно и без костылей не поддерживает cross- join.
    cross_joined = []

    for i in range(len(user_point_sums)):
        for j in range(len(user_point_sums)):
            if i==j:
                continue
            cross_joined.append({
                'user_id_1': user_point_sums[i][0],
                'user_id_2': user_point_sums[j][0],
                'difference': abs(user_point_sums[i][1] - user_point_sums[j][1])
            })

    result = min(cross_joined, key = lambda k: k['difference'])

    return [result['user_id_1'], result['user_id_2']]


@users_router.get("/users/achievements_7_days_in_row")
def get_users_with_achievements_7_days_in_row(session: Session = Depends(get_session)):
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=7)


    stmt = select(UserAchievement).filter(UserAchievement.awarding_datetime >= start_date, UserAchievement.awarding_datetime <= end_date)

    result = session.execute(stmt)

    return result.all()


add_pagination(users_router)


class Pydantic_Ach_With_Translation(BaseModel):
    name: str
    description: str


class Pydanticachievement(BaseModel):
    id: int
    points: int
    ru_achievement: Pydantic_Ach_With_Translation
    en_achievement: Pydantic_Ach_With_Translation


@achievement_router.get("/")
def get_all_achievements(session: Session = Depends(get_session)) -> Page[Pydanticachievement]:
    stmt = select(Achievement)

    return paginate(session, stmt)


@achievement_router.post("/")
def create_new_achievement(points: int,
                          name_ru: str,
                          name_en: str,
                          ru_description: str,
                          en_description: str,
                          session: Session = Depends(get_session)):

    en_ach = EN_achievement(name=name_en,
                            description=en_description)

    ru_ach = RU_achievement(name=name_ru,
                            description=ru_description)

    new_achievement = Achievement(points=points,
                                  ru_achievement=ru_ach,
                                  en_achievement=en_ach)

    session.add(new_achievement)
    session.commit()


add_pagination(achievement_router)
