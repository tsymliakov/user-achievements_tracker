from typing import List

from datetime import datetime

from sqlalchemy import ForeignKey, Column, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
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

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    points: Mapped[int] = mapped_column(nullable=False)

    achievment_of_user: Mapped[List["User"]] = relationship(
        back_populates="user_achievments",
        secondary="user_achievment"
    )

    ru_achievment: Mapped['RU_achievment'] = relationship(back_populates='achievment')
    en_achievment: Mapped['EN_achievment'] = relationship(back_populates='achievment')


class RU_achievment(Base):
    __tablename__ = "ru_achievments"

    parent_ach_id: Mapped[int] = mapped_column(ForeignKey(Achievment.id))
    name: Mapped[str] = mapped_column(nullable=False, primary_key=True)
    description: Mapped[str] = mapped_column(nullable=False)
    achievment: Mapped[Achievment] = relationship(back_populates='ru_achievment')


class EN_achievment(Base):
    __tablename__ = "en_achievments"

    parent_ach_id: Mapped[int] = mapped_column(ForeignKey(Achievment.id))
    name: Mapped[str] = mapped_column(nullable=False, primary_key=True)
    description: Mapped[str] = mapped_column(nullable=False)
    achievment: Mapped[Achievment] = relationship(back_populates='en_achievment')


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
    awarding_datetime = Column(DateTime, default=datetime.utcnow, nullable=False)
