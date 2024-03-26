from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


from src.config import DB_HOST, DB_PORT, POSTGRES_DB, POSTGRES_PASSWORD, POSTGRES_USER


DATABASE_URL = f"postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:{DB_PORT}/{POSTGRES_DB}"


class Base(DeclarativeBase):
    pass


engine = create_engine(DATABASE_URL, echo=True)

Session = sessionmaker(engine)
