from sqlalchemy import create_engine
from config import settings
from models import Base


engine = create_engine(
    url = settings.DATABASE_URL_psycopg,
    echo=True,
)

Base.metadata.create_all(engine)
