import logging
from app.utils import Response
from fastapi import APIRouter, Depends
from app.schemas import CreateUserReq
from sqlalchemy.ext.asyncio import AsyncSession
from app.storages import get_db_session
from app.services import UserService
from app.utils import create_token

logger = logging.getLogger(__name__)

router = APIRouter(
  prefix="/user",
  tags=["用户模块"]
)


@router.post(path="/register", response_model=Response, summary="用户注册", description="用户注册")
async def register(user: CreateUserReq, db_session: AsyncSession = Depends(get_db_session)) -> Response:
  user = await UserService.register(db_session, user)
  return Response.success(msg="用户注册成功", data={"username": user.username})


@router.post(path="/login", response_model=Response, summary="用户登录", description="用户登录")
async def login(user: CreateUserReq, db_session: AsyncSession = Depends(get_db_session)) -> Response:
  user = await UserService.login(db_session, user)
  token = create_token({"sub": str(user.id), "username": user.username})
  return Response.success(msg="用户登录成功", data={
    "username": user.username,
    "token": token
  })
