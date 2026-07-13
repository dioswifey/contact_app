"""
crud.py — DB 작업 함수: 조회/생성/수정/삭제 (핵심 로직)
TRD §4, §6 참조.
원칙: 이 파일의 모든 조회 함수는 첫 번째 규칙으로 user_id를 조건에 포함한다(데이터 격리).
이 파일은 상태 코드를 모른다 — None/bool 등 순수 데이터만 반환한다.
"""
import secrets

from sqlalchemy import select, func
from sqlalchemy.orm import Session

import models
import schemas
from security import hash_password, verify_password

DEFAULT_CATEGORIES = ["가족", "친구", "기타"]


# ── 인증 ──────────────────────────────────────────────
def get_user_by_username(db: Session, username: str) -> models.User | None:
    return db.scalar(select(models.User).where(models.User.username == username))


def create_user(db: Session, data: schemas.SignupIn) -> models.User:
    user = models.User(username=data.username, password_hash=hash_password(data.password))
    db.add(user)
    db.flush()  # user.id 확보

    for name in DEFAULT_CATEGORIES:
        db.add(models.Category(user_id=user.id, name=name))

    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, username: str, password: str) -> models.User | None:
    user = get_user_by_username(db, username)
    if user is None or not verify_password(password, user.password_hash):
        return None
    return user


def create_login_session(db: Session, user_id: int) -> str:
    token = secrets.token_hex(32)
    db.add(models.LoginSession(session_id=token, user_id=user_id))
    db.commit()
    return token


def get_user_by_session(db: Session, session_id: str) -> models.User | None:
    session = db.get(models.LoginSession, session_id)
    if session is None:
        return None
    return db.get(models.User, session.user_id)


def delete_login_session(db: Session, session_id: str) -> None:
    session = db.get(models.LoginSession, session_id)
    if session is not None:
        db.delete(session)
        db.commit()


# ── 카테고리 ──────────────────────────────────────────
def list_categories(db: Session, user_id: int) -> list[models.Category]:
    stmt = select(models.Category).where(models.Category.user_id == user_id).order_by(models.Category.id)
    return list(db.scalars(stmt))


def get_my_category(db: Session, user_id: int, category_id: int) -> models.Category | None:
    stmt = select(models.Category).where(
        models.Category.id == category_id, models.Category.user_id == user_id
    )
    return db.scalar(stmt)


def category_name_exists(db: Session, user_id: int, name: str, exclude_id: int | None = None) -> bool:
    stmt = select(models.Category).where(models.Category.user_id == user_id, models.Category.name == name)
    if exclude_id is not None:
        stmt = stmt.where(models.Category.id != exclude_id)
    return db.scalar(stmt) is not None


def create_category(db: Session, user_id: int, data: schemas.CategoryCreate) -> models.Category:
    category = models.Category(user_id=user_id, name=data.name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def update_category(db: Session, category: models.Category, data: schemas.CategoryUpdate) -> models.Category:
    category.name = data.name
    db.commit()
    db.refresh(category)
    return category


def count_contacts_in_category(db: Session, user_id: int, category_id: int) -> int:
    stmt = select(func.count()).select_from(models.Contact).where(
        models.Contact.user_id == user_id, models.Contact.category_id == category_id
    )
    return db.scalar(stmt) or 0


def delete_category(db: Session, category: models.Category) -> None:
    db.delete(category)
    db.commit()


# ── 연락처 ────────────────────────────────────────────
def _to_out(contact: models.Contact) -> schemas.ContactOut:
    return schemas.ContactOut(
        id=contact.id,
        name=contact.name,
        phone=contact.phone,
        addr=contact.addr,
        category_id=contact.category_id,
        category_name=contact.category.name,
    )


def list_contacts(
    db: Session, user_id: int, name: str | None = None, category_id: int | None = None
) -> list[schemas.ContactOut]:
    stmt = select(models.Contact).where(models.Contact.user_id == user_id)
    if name:
        stmt = stmt.where(models.Contact.name == name)
    if category_id:
        stmt = stmt.where(models.Contact.category_id == category_id)
    stmt = stmt.order_by(models.Contact.id)
    return [_to_out(c) for c in db.scalars(stmt)]


def get_my_contact(db: Session, user_id: int, contact_id: int) -> models.Contact | None:
    stmt = select(models.Contact).where(
        models.Contact.id == contact_id, models.Contact.user_id == user_id
    )
    return db.scalar(stmt)


def phone_exists(db: Session, user_id: int, phone: str, exclude_id: int | None = None) -> bool:
    stmt = select(models.Contact).where(models.Contact.user_id == user_id, models.Contact.phone == phone)
    if exclude_id is not None:
        stmt = stmt.where(models.Contact.id != exclude_id)
    return db.scalar(stmt) is not None


def create_contact(db: Session, user_id: int, data: schemas.ContactCreate) -> schemas.ContactOut:
    contact = models.Contact(user_id=user_id, **data.model_dump())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return _to_out(contact)


def update_contact(db: Session, contact: models.Contact, data: schemas.ContactUpdate) -> schemas.ContactOut:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(contact, field, value)
    db.commit()
    db.refresh(contact)
    return _to_out(contact)


def delete_contact(db: Session, contact: models.Contact) -> None:
    db.delete(contact)
    db.commit()
