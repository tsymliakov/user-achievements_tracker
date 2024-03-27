from fastapi import FastAPI
from src.presentation.rest.routers import users_router, achievment_router


app = FastAPI()


app.include_router(users_router)
app.include_router(achievment_router)


@app.get("/")
def main():
    return {"data": "Hello!"}
