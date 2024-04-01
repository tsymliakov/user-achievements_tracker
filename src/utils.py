import sys
import os

par_dir = os.path.dirname(__file__)
project_dir = os.path.dirname(par_dir)

sys.path.insert(0, project_dir)

from src.models import *
from src.database import session_factory

from datetime import datetime, timedelta

import random

from faker import Faker
from faker.providers import DynamicProvider


achievements = [
    {
        'points' : 1,
        'ru': {
            'name': 'Первый шутник на районе',
            'description': 'Пошутил смешнее остальных'
        },
        'en': {
            'name': 'First jokester in the neighborhood',
            'description': 'Made the funniest joke of all'
        }
    },
    {
        'points' : 2,
        'ru': {
            'name': 'Участник допинг- контроля',
            'description': 'Прошел все unit-тесты самостоятельно без участия кода'
        },
        'en': {
            'name': 'Doping Control Participant',
            'description': 'Passed all unit tests independently without code participation'
        }
    },
    {
        'points' : 3,
        'ru': {
            'name': 'Бабушкино золотце',
            'description': 'Grandma\'s goldfish'
        },
        'en': {
            'name': 'Съел первое, второе, компот и попросил добавки',
            'description': 'Ate the first and second course, compote and asked for more'
        }
    }
]


def _create_fake_users():
    language_provider = DynamicProvider(
        provider_name="language",
        elements = ["ru", "en"]
    )

    f = Faker()
    f.add_provider(language_provider)

    with session_factory() as session:
        for _ in range(3):
            new_user = User(name=f.name(), language=f.language())
            session.add(new_user)
        session.commit()


def _create_fake_achievements():
    global achievements

    with session_factory() as session:
        for ach in achievements:
            r_ach = RU_achievement(**ach['ru'])
            e_ach = EN_achievement(**ach['en'])
            achievement = Achievement(points=ach['points'], ru_achievement=r_ach, en_achievement=e_ach)
            session.add(achievement)
        session.commit()


def _random_past_date():
    return datetime.utcnow() - timedelta(days=random.randint(0, 365))


def _assign_achievements_to_users():
    with session_factory() as session:
        users = session.query(User).all()
        achievements = session.query(Achievement).all()

        for user in users:
            num_achievements = random.randint(1, 3)

            selected_achievements = random.sample(achievements, num_achievements)
            for ach in selected_achievements:
                user_achievement = Userachievement(user_id=user.id,
                                                 achievement_id=ach.id,
                                                 awarding_datetime=_random_past_date())

                session.add(user_achievement)
        session.commit()


def _clear_tables():
    with session_factory() as session:
        session.query(Userachievement).delete()
        session.query(User).delete()
        session.query(RU_achievement).delete()
        session.query(EN_achievement).delete()
        session.query(Achievement).delete()
        session.commit()


def _fill_tables():
    _create_fake_users()
    _create_fake_achievements()
    _assign_achievements_to_users()



def prepare_tables(clear_tables=False):
    if clear_tables:
        _clear_tables()
    _fill_tables()
