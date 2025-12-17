from datetime import datetime, timedelta, timezone
from backend.src.config import settings

from passlib.context import CryptContext

import jwt

pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    pbkdf2_sha256__default_rounds=600000,
    pbkdf2_sha256__salt_size=16,
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        weeks=settings.ACCESS_TOKEN_EXPIRE_WEEKS
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt
