from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from src.config import settings

engine = create_engine(
    url=settings.DATABASE_URL,
    echo=True,
)

session_factory = sessionmaker(engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = session_factory()
    try:
        yield db
    finally:
        db.close()
