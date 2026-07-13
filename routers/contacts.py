"""
routers/contacts.py — 연락처 엔드포인트 4개
라우터는 "접수 → 확인 → crud 호출 → 응답 포장"만 한다. DB 코드는 직접 쓰지 않는다.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import get_db
from routers.auth import get_current_user

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("", response_model=schemas.ContactListOut)
def list_contacts(
    name: str | None = None,
    category_id: int | None = None,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    items = crud.list_contacts(db, user.id, name=name, category_id=category_id)
    return schemas.ContactListOut(total=len(items), items=items)


@router.post("", response_model=schemas.ContactOut, status_code=201)
def add_contact(
    data: schemas.ContactCreate,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if crud.get_my_category(db, user.id, data.category_id) is None:
        raise HTTPException(status_code=404, detail="해당 카테고리가 없습니다")
    if crud.phone_exists(db, user.id, data.phone):
        raise HTTPException(status_code=409, detail="이미 등록된 전화번호입니다")
    return crud.create_contact(db, user.id, data)


@router.patch("/{contact_id}", response_model=schemas.ContactOut)
def edit_contact(
    contact_id: int,
    data: schemas.ContactUpdate,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    contact = crud.get_my_contact(db, user.id, contact_id)
    if contact is None:
        raise HTTPException(status_code=404, detail="해당 연락처가 없습니다")

    if data.category_id is not None and crud.get_my_category(db, user.id, data.category_id) is None:
        raise HTTPException(status_code=404, detail="해당 카테고리가 없습니다")
    if data.phone is not None and crud.phone_exists(db, user.id, data.phone, exclude_id=contact_id):
        raise HTTPException(status_code=409, detail="이미 등록된 전화번호입니다")

    return crud.update_contact(db, contact, data)


@router.delete("/{contact_id}", status_code=204)
def remove_contact(
    contact_id: int,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    contact = crud.get_my_contact(db, user.id, contact_id)
    if contact is None:
        raise HTTPException(status_code=404, detail="해당 연락처가 없습니다")
    crud.delete_contact(db, contact)
