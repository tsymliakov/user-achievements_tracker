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


achievments = [
        {
            'points' : 1,
            'name_ru' : 'Первый шутник на районе',
            'name_en' : 'First jokester in the neighborhood',
            'ru_description' : 'Пошутил смешнее остальных',
            'en_description' : 'Made the funniest joke of all'
        },
        {
            'points' : 2,
            'name_ru' : 'Участник допинг- контроля',
            'name_en' : 'Doping Control Participant',
            'ru_description' : 'Прошел все unit-тесты самостоятельно без участия кода',
            'en_description' : 'Passed all unit tests independently without code participation'
        },{
            'points' : 3,
            'name_ru' : 'Бабушкино золотце',
            'name_en' : 'Grandma\'s goldfish',
            'ru_description' : 'Съел первое, второе, компот и попросил добавки',
            'en_description' : 'Ate the first, second, compote and asked for more'
        }
    ]


def _create_fake_users():
    language_provider = DynamicProvider(
        provider_name="language",
        elements = ["ru_description", "en"]
    )

    f = Faker()
    f.add_provider(language_provider)

    with session_factory() as session:
        for _ in range(3):
            new_user = User(name=f.name(), language=f.language())
            session.add(new_user)
        session.commit()


def _create_fake_achievments():
    global achievments

    with session_factory() as session:
        for ach in achievments:
            session.add(Achievment(**ach))
        session.commit()


def _random_past_date():
    return datetime.utcnow() - timedelta(days=random.randint(0, 365))


def _assign_achievements_to_users():
    with session_factory() as session:
        users = session.query(User).all()
        achievments = session.query(Achievment).all()

        for user in users:
            num_achievements = random.randint(1, 3)

            selected_achievments = random.sample(achievments, num_achievements)
            for ach in selected_achievments:
                user_achievment = UserAchievment(user_id=user.id,
                                                 achievment_id=ach.id,
                                                 awarding_datetime=_random_past_date())

                session.add(user_achievment)
        session.commit()


def _clear_tables():
    with session_factory() as session:
        session.query(UserAchievment).delete()
        session.query(User).delete()
        session.query(Achievment).delete()
        session.commit()


def _fill_tables():
    _create_fake_users()
    _create_fake_achievments()
    _assign_achievements_to_users()



def prepare_tables(clear_tables=False):
    if clear_tables:
        _clear_tables()
    _fill_tables()



