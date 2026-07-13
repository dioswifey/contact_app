"""
security.py — 비밀번호 해싱/대조 (TRD §5-3)
"비밀번호 다루는 코드가 여기 다 있다"를 보장하는 파일. 해싱 방식을 바꿔도 이 파일만 고치면 된다.
"""
from pwdlib import PasswordHash

_password_hash = PasswordHash.recommended()  # Argon2id 기본


def hash_password(plain_password: str) -> str:
    return _password_hash.hash(plain_password)


def verify_password(plain_password: str, password_hash: str) -> bool:
    return _password_hash.verify(plain_password, password_hash)
