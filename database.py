"""
database.py — DB 연결: engine, SessionLocal, get_db
TRD §6 참조
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 환경변수로 접속정보를 오버라이드할 수 있게 함 (기본값은 로컬 pg-lab 컨테이너 기준)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:postgres@localhost:5432/contactdb",
)

# Railway가 주입하는 DATABASE_URL은 드라이버 없는 "postgresql://" 스킴이라
# SQLAlchemy가 기본으로 psycopg2를 찾는데, 설치돼 있는 건 psycopg(3)뿐이라 임포트가 실패한다.
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """요청마다 DB 세션을 열어 빌려주고(yield), 끝나면 반드시 닫는다."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
