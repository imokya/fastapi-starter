from datetime import datetime, timedelta, timezone

from jwt import encode, decode
from app.config import get_settings


def create_token(data: dict) -> str:
  settings = get_settings()
  to_encode = data.copy()
  expire = datetime.now(timezone.utc) + timedelta(seconds=settings.jwt_expire_time)
  to_encode["exp"] = expire
  return encode(
    to_encode,
    settings.jwt_secret_key,
    algorithm=settings.jwt_algorithm,
  )


def verify_token(token: str) -> dict:
  settings = get_settings()
  return decode(
    token,
    settings.jwt_secret_key,
    algorithms=[settings.jwt_algorithm]
  )
