from fastapi import Depends
from app.utils import verify_token
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from app.errors import UnauthorizedError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")


def auth_user(token: str = Depends(oauth2_scheme)) -> dict:
  """验证JWT token是否有效"""
  try:
    payload = verify_token(token)
  except InvalidTokenError:
    raise UnauthorizedError("无效的token")
  except ExpiredSignatureError:
    raise UnauthorizedError("token已过期")

  if not payload:
    raise UnauthorizedError("无效的token")
  return payload
