from typing import List

from datetime import datetime

from typing_extensions import Annotated

from sqlalchemy import ForeignKey, Column, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


timestamp = Annotated[
    datetime,
    mapped_column(nullable=False)
]


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    language: Mapped[str] = mapped_column(nullable=False)

    user_achievments: Mapped[List["Achievment"]] = relationship(
        back_populates="achievment_of_user",
        secondary="user_achievment"
    )

    def __str__(self):
        return {"id" : self.id,
                "name" : self.name,
                "language": self.language}


class Achievment(Base):
    __tablename__ = "achievments"

    id: Mapped[int] = mapped_column(primary_key=True)
    points: Mapped[int] = mapped_column(nullable=False)
    name_ru: Mapped[str] = mapped_column(nullable=False, primary_key=True)
    name_en: Mapped[str] = mapped_column(nullable=False, primary_key=True)
    ru_description: Mapped[str] = mapped_column(nullable=False)
    en_description: Mapped[str] = mapped_column(nullable=False)

    achievment_of_user: Mapped[List["User"]] = relationship(
        back_populates="user_achievments",
        secondary="user_achievment"
    )


class UserAchievment(Base):
    __tablename__ = "user_achievment"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        primary_key=True,
    )
    achievment_id: Mapped[int] = mapped_column(
        ForeignKey("achievments.id"),
        primary_key=True,
    )
    awarding_datetime = Column(DateTime, default=datetime.utcnow)
