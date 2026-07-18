import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.logging import setup_logging
from app.routers.router import router
from app.storages import get_redis, get_postgres, get_cos
from app.errors import register_exception_handlers

# 加载配置信息
settings = get_settings()

# 初始化日志系统
setup_logging()

logger = logging.getLogger()

# 定义FastAPI路由tags标签
openapi_tags = [
  {
    "name": "状态模块",
    "description": "包含 **状态监测** 等API接口，用于监测系统的运行状态。"
  }
]


async def lifespan(app: FastAPI):
  """创建FastAPI应用程序生命周期上下文管理"""
  logger.info("应用启动中...")

  # 初始化redis客户端
  await get_redis().init()
  # 初始化postgres连接
  await get_postgres().init()
  # 初始化腾讯云COS客户端
  await get_cos().init()

  try:
    yield
  finally:
    # 关闭redis客户端
    await get_redis().shutdown()
    await get_postgres().shutdown()
    await get_cos().shutdown()
    logger.info("应用关闭中...")

# 创建FastAPI应用实例
app = FastAPI(
  title="行歌通用智能体",
  description="行歌通用智能体API接口文档",
  version="1.0.0",
  openapi_tags=openapi_tags,
  lifespan=lifespan
)

# 注册CORS跨域中间件
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

# 注册异常处理
register_exception_handlers(app)

# 注册API路由
app.include_router(router, prefix="/api")
