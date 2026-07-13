"""
main.py — 앱 조립: FastAPI 생성, 라우터 등록, 화면 제공
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from database import Base, engine
from routers import auth, contacts, categories

Base.metadata.create_all(bind=engine)

app = FastAPI(title="연락처 관리 웹 서비스")

app.include_router(auth.router)
app.include_router(contacts.router)
app.include_router(categories.router)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def index():
    return FileResponse("static/index.html")
