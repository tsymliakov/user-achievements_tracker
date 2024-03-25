from fastapi import FastAPI

import database


app = FastAPI()


@app.get("/")
def main():
    return {"data": "Hello!"}

# Инофрмация о пользователе
@app.get("/users/{id}")
def get_user(id):
    return f"User: {id}"

# Все доступные достижения
@app.get("/achievments")
def get_all_achievments():
    return "Achievments"

# Добавить новое достижение
@app.post("/achievments/add")
def add_achievment():
    pass

# Добавить пользователю достижение
@app.post("/users/{user_id}/{achievment_id}")
def add_achievment_to_user():
    pass

# предоставлять информацию о выданных пользователю достижениях на выбранном пользователем языке

# Пользователь с максимальным количеством достижений
@app.get("/users/max_achievments")
def get_user_max_achievments():
    pass

# Пользователь с максимальным количеством очков достижений;
@app.get("/users/max_score")
def get_user_max_score():
    pass

# Пользователи с максимальной разностью очков достижений;
@app.get("/users/max_difference_score")
def get_users_max_diff():
    pass

# Пользователи с минимальной разностью очков достижений;
@app.get("/users/min_difference_score")
def get_users_min_diff():
    pass

# Пользователи, у которых достижения выдавались 7 дней подряд (есть достижения с датами выдачи соответсвующими)
