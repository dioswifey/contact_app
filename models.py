"""
models.py — 테이블 정의: User, LoginSession, Category, Contact
TRD §3 참조. "세션" 이름 충돌을 피하려고 로그인 세션 모델은 LoginSession으로 명명한다.
"""
from datetime import datetime

from sqlalchemy import String, ForeignKey, UniqueConstraint, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    sessions: Mapped[list["LoginSession"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    categories: Mapped[list["Category"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    contacts: Mapped[list["Contact"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class LoginSession(Base):
    __tablename__ = "sessions"

    session_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="sessions")


class Category(Base):
    __tablename__ = "categories"
    __table_args__ = (UniqueConstraint("user_id", "name", name="uq_user_category_name"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(30), nullable=False)

    user: Mapped["User"] = relationship(back_populates="categories")
    contacts: Mapped[list["Contact"]] = relationship(back_populates="category")


class Contact(Base):
    __tablename__ = "contacts"
    __table_args__ = (UniqueConstraint("user_id", "phone", name="uq_user_phone"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    addr: Mapped[str | None] = mapped_column(String(255), nullable=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="contacts")
    category: Mapped["Category"] = relationship(back_populates="contacts")
