from fastapi import APIRouter
from app.utils import Response, auth_user
from fastapi import Depends


router = APIRouter(prefix="/session", tags=["会话模块"])


@router.post(path="/chat", response_model=Response, summary="聊天会话", description="聊天会话")
async def chat(user: dict = Depends(auth_user)) -> Response:
  return Response.success()
