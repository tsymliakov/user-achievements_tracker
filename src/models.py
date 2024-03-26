from typing import List

from datetime import datetime

from sqlalchemy import ForeignKey, Integer, Table, Column, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base




User_Achievment = Table(
    "user_achievment",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("users.id")),
    Column("achievment_id", ForeignKey("achievments.id")),
    Column("awarding_datetime", TIMESTAMP, default=datetime.utcnow())
)


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    language: Mapped[str] = mapped_column(nullable=False)

    user_achievments: Mapped[List["Achievment"]] = relationship(
        back_populates="achievment_of_user",
        secondary='user_achievment'
    )


class Achievment(Base):
    __tablename__ = 'achievments'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    points: Mapped[int] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)

    achievment_of_user: Mapped[List["User"] = mapped]

    users: Mapped[int] = relationship(
        'users',
        secondary=User_Achievment,
        backref='achievments')


class UserAchievments(Base):
    __tablename__ = 'user_achievment'

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        primary_key=True,
    )
    achievment_id: Mapped[int] = mapped_column(
        ForeignKey("achievments.id"),
        primary_key=True,
    )
    awarding_datetime: Mapped[TIMESTAMP]
