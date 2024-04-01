from fastapi import FastAPI
from src.presentation.rest.routers import users_router, achievment_router
from src.utils import prepare_tables

from src.config import DEVELOPMENT, CLEAR_TABLES


if DEVELOPMENT:
    prepare_tables(clear_tables=CLEAR_TABLES)


app = FastAPI()


app.include_router(users_router)
app.include_router(achievment_router)


@app.get("/")
def main():
    return {"data": "Hello!"}
