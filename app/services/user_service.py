from sqlalchemy import exists, select
from app.models import User
from app.schemas.user_schema import CreateUserReq
from sqlalchemy.ext.asyncio import AsyncSession
from app.errors import ValidationError
from app.utils import hash_password, verify_password


class UserService:

  @staticmethod
  async def register(db_session: AsyncSession, user: CreateUserReq) -> User:

    # 判断用户名是否已经存在
    check_user_exists = await db_session.execute(
      select(exists().where(User.username == user.username))
    )
    if check_user_exists.scalar():
      raise ValidationError("用户名已存在")

    db_user = User(
      username=user.username,
      password=hash_password(user.password),
      email="",
      openid="",
    )
    db_session.add(db_user)
    await db_session.flush()
    return db_user

  @staticmethod
  async def login(db_session: AsyncSession, user: CreateUserReq) -> User:
    result = await db_session.execute(
      select(User).where(User.username == user.username)
    )
    db_user = result.scalars().first()
    if not db_user or not verify_password(user.password, db_user.password):
      raise ValidationError("用户名或密码错误")
    return db_user
