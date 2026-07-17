from fastapi.routing import APIRouter
from app.routers import status_router


def create_api_routes() -> APIRouter:
  """创建API路由，涵盖整个项目的所有路由管理"""

  # 创建APIRouter实例
  api_router = APIRouter()

  # 将各个模块的路由注册到APIRouter实例
  api_router.include_router(status_router.router)

  return api_router


router = create_api_routes()
