from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    position: Mapped[str] = mapped_column(String(100), nullable=False)
    referral_token: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    referral_link: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    referral: Mapped["Referral"] = relationship(back_populates="referrer", uselist=False, cascade="all, delete-orphan")
    rewards: Mapped[list["RewardSystem"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class Referral(Base):
    __tablename__ = "referrals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    referrer_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True, nullable=False)
    referral_token: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    referral_link: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    user_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    referrer: Mapped[User] = relationship(back_populates="referral")


class RewardSystem(Base):
    __tablename__ = "reward_system"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    referral_id: Mapped[int] = mapped_column(ForeignKey("referrals.id"), nullable=False)
    reward_points: Mapped[int] = mapped_column(Integer, default=10, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user: Mapped[User] = relationship(back_populates="rewards")
