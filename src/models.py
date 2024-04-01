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

    user_achievements: Mapped[List["Achievement"]] = relationship(
        back_populates="achievement_of_user",
        secondary="user_achievement"
    )

    def __str__(self):
        return {"id" : self.id,
                "name" : self.name,
                "language": self.language}


class Achievement(Base):
    __tablename__ = "achievements"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    points: Mapped[int] = mapped_column(nullable=False)

    achievement_of_user: Mapped[List["User"]] = relationship(
        back_populates="user_achievements",
        secondary="user_achievement"
    )

    ru_achievement: Mapped['RU_achievement'] = relationship(back_populates='achievement')
    en_achievement: Mapped['EN_achievement'] = relationship(back_populates='achievement')


class RU_achievement(Base):
    __tablename__ = "ru_achievements"

    parent_ach_id: Mapped[int] = mapped_column(ForeignKey(Achievement.id))
    name: Mapped[str] = mapped_column(nullable=False, primary_key=True)
    description: Mapped[str] = mapped_column(nullable=False)
    achievement: Mapped[Achievement] = relationship(back_populates='ru_achievement')


class EN_achievement(Base):
    __tablename__ = "en_achievements"

    parent_ach_id: Mapped[int] = mapped_column(ForeignKey(Achievement.id))
    name: Mapped[str] = mapped_column(nullable=False, primary_key=True)
    description: Mapped[str] = mapped_column(nullable=False)
    achievement: Mapped[Achievement] = relationship(back_populates='en_achievement')


class UserAchievement(Base):
    __tablename__ = "user_achievement"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        primary_key=True,
    )
    achievement_id: Mapped[int] = mapped_column(
        ForeignKey("achievements.id"),
        primary_key=True,
    )
    awarding_datetime = Column(DateTime, default=datetime.utcnow, nullable=False)
