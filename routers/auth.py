"""
routers/auth.py — 인증 엔드포인트 4개 + get_current_user 의존성 (2차 과제의 심장)
TRD §5 참조.
"""
from fastapi import APIRouter, Depends, HTTPException, Response, Cookie
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


def get_current_user(
    session_id: str | None = Cookie(default=None),
    db: Session = Depends(get_db),
) -> models.User:
    if session_id is None:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다")

    user = crud.get_user_by_session(db, session_id)
    if user is None:
        raise HTTPException(status_code=401, detail="세션이 만료되었거나 유효하지 않습니다")

    return user


@router.post("/signup", response_model=schemas.UserOut, status_code=201)
def signup(data: schemas.SignupIn, db: Session = Depends(get_db)):
    if crud.get_user_by_username(db, data.username) is not None:
        raise HTTPException(status_code=409, detail="이미 사용 중인 아이디입니다")
    user = crud.create_user(db, data)
    return user


@router.post("/login", response_model=schemas.UserOut)
def login(data: schemas.LoginIn, response: Response, db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, data.username, data.password)
    if user is None:
        raise HTTPException(status_code=401, detail="아이디 또는 비밀번호가 올바르지 않습니다")

    token = crud.create_login_session(db, user.id)
    response.set_cookie("session_id", token, httponly=True, samesite="lax")
    return user


@router.post("/logout", status_code=204)
def logout(
    response: Response,
    session_id: str | None = Cookie(default=None),
    db: Session = Depends(get_db),
):
    if session_id:
        crud.delete_login_session(db, session_id)
    response.delete_cookie("session_id")


@router.get("/me", response_model=schemas.UserOut)
def me(user: models.User = Depends(get_current_user)):
    return user
