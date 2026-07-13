"""
routers/categories.py — 카테고리 엔드포인트 4개
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import get_db
from routers.auth import get_current_user

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("", response_model=list[schemas.CategoryOut])
def list_categories(
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return crud.list_categories(db, user.id)


@router.post("", response_model=schemas.CategoryOut, status_code=201)
def add_category(
    data: schemas.CategoryCreate,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if crud.category_name_exists(db, user.id, data.name):
        raise HTTPException(status_code=409, detail="이미 있는 종류 이름입니다")
    return crud.create_category(db, user.id, data)


@router.patch("/{category_id}", response_model=schemas.CategoryOut)
def edit_category(
    category_id: int,
    data: schemas.CategoryUpdate,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    category = crud.get_my_category(db, user.id, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="해당 카테고리가 없습니다")
    if crud.category_name_exists(db, user.id, data.name, exclude_id=category_id):
        raise HTTPException(status_code=409, detail="이미 있는 종류 이름입니다")
    return crud.update_category(db, category, data)


@router.delete("/{category_id}", status_code=204)
def remove_category(
    category_id: int,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    category = crud.get_my_category(db, user.id, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="해당 카테고리가 없습니다")

    n = crud.count_contacts_in_category(db, user.id, category_id)
    if n > 0:
        raise HTTPException(
            status_code=409,
            detail=f"이 카테고리를 사용하는 연락처가 {n}건 있어 삭제할 수 없습니다. 연락처의 종류를 먼저 변경하세요.",
        )
    crud.delete_category(db, category)
