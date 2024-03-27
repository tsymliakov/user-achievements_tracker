import sys
import os

par_dir = os.path.dirname(__file__)
project_dir = os.path.dirname(par_dir)

sys.path.insert(0, project_dir)

from src.models import *
from src.database import Session

from sqlalchemy import select

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


def create_fake_users():
    language_provider = DynamicProvider(
        provider_name="language",
        elements = ["ru_description", "en"]
    )

    f = Faker()
    f.add_provider(language_provider)

    with Session() as session:
        for _ in range(1000):
            new_user = User(name=f.name(), language=f.language())
            session.add(new_user)
        session.commit()


def create_fake_achievments():
    global achievments

    with Session() as session:
        for ach in achievments:
            session.add(Achievment(**ach))
        session.commit()
