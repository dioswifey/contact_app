"""
schemas.py — 입출력 양식: Pydantic 모델 (검증 규칙의 집)
TRD §8 참조. "받을 것"과 "보여줄 것"은 항상 다른 양식으로 분리한다.
"""
from pydantic import BaseModel, Field, ConfigDict


# ── 인증 ──────────────────────────────────────────────
class SignupIn(BaseModel):
    username: str = Field(pattern=r"^[A-Za-z][A-Za-z0-9_-]{2,29}$", min_length=3, max_length=30)
    password: str = Field(min_length=4, max_length=20)


class LoginIn(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str


# ── 카테고리 ──────────────────────────────────────────
class CategoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=10)


class CategoryUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=10)


class CategoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str


# ── 연락처 ────────────────────────────────────────────
class ContactCreate(BaseModel):
    name: str = Field(min_length=1, max_length=5)
    phone: str = Field(pattern=r"^010\d{8}$")
    addr: str | None = None
    category_id: int


class ContactUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=5)
    phone: str | None = Field(default=None, pattern=r"^010\d{8}$")
    addr: str | None = None
    category_id: int | None = None


class ContactOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    phone: str
    addr: str | None
    category_id: int
    category_name: str


class ContactListOut(BaseModel):
    total: int
    items: list[ContactOut]
