from fastapi import FastAPI
from src.database import Session

from src.models import User, Achievment, User_Achievment


app = FastAPI()


@app.get("/")
def main():
    return {"data": "Hello!"}

# @app.get("/users/")
# def get_users():
#     with Session() as session:
#         users = session.query(TestUser).all()
#     return users

# @app.get("/users/add")
# def add_user():
#     with Session() as session:
#         new_user = TestUser(name="John")
#         session.add(new_user)
#         session.commit()


# Информация о пользователе
@app.get("/users/{id}")
def get_user(id: int):
    with Session() as session:
        user = session.query(User).all()
    return user


# # Все доступные достижения
# @app.get("/achievments")
# def get_all_achievments():
#     return "Achievments"

# # Добавить новое достижение
# @app.post("/achievments/add")
# def add_achievment():
#     pass

# # Добавить пользователю достижение
# @app.post("/users/{user_id}/{achievment_id}")
# def add_achievment_to_user():
#     pass

# # предоставлять информацию о выданных пользователю достижениях на выбранном пользователем языке

# # Пользователь с максимальным количеством достижений
# @app.get("/users/max_achievments")
# def get_user_max_achievments():
#     pass

# # Пользователь с максимальным количеством очков достижений;
# @app.get("/users/max_score")
# def get_user_max_score():
#     pass

# # Пользователи с максимальной разностью очков достижений;
# @app.get("/users/max_difference_score")
# def get_users_max_diff():
#     pass

# # Пользователи с минимальной разностью очков достижений;
# @app.get("/users/min_difference_score")
# def get_users_min_diff():
#     pass

# # Пользователи, у которых достижения выдавались 7 дней подряд (есть достижения с датами выдачи соответсвующими)
