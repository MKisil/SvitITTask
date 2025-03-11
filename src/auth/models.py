from sqlalchemy import Column, Integer, String

from src.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(length=255), unique=True, index=True)
    password = Column(String)