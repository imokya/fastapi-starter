import logging
from typing import Optional
from app.config import get_settings, Settings
from sqlalchemy.ext.asyncio import (
  AsyncEngine,
  async_sessionmaker,
  create_async_engine,
  AsyncSession
)
from sqlalchemy import text
from functools import lru_cache


logger = logging.getLogger(__name__)


class Postgress:
  """Postgres数据库基础类，用于完成数据库连接等配置操作"""

  def __init__(self):
    """构造函数，完成postgres数据库引擎，会话工厂的创建"""
    self._engine: Optional[AsyncEngine] = None
    self._session_factory: Optional[async_sessionmaker] = None
    self._settings: Settings = get_settings()

  async def init(self) -> None:
    """初始化postgres连接"""
    # 判断引擎是否存在，如果存在则表示已经连上，无需重复连接
    if self._engine is not None:
      logger.warning("Postgres数据库引擎已经初始化，无需重复连接")
      return

    try:
      # 创建异步引擎
      logger.info("正在初始化Postgres连接")
      self._engine = create_async_engine(
        self._settings.sqlalchemy_database_url,
        echo=True if self._settings.env == "development" else False
      )

      # 创建会话工厂
      self._session_factory = async_sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=self._engine
      )
      logger.info("Postgres会话工厂创建完毕")

      # 连接Postgres并进行预操作
      async with self._engine.begin() as async_conn:
        await async_conn.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'))
        logger.info("Postgres成功连接并安装uuid-ossp扩展")
    except Exception as e:
      logger.error(f"Postgres数据库引擎初始化失败: {str(e)}")
      raise e

  async def shutdown(self) -> None:
    """关闭Postgres连接"""
    if self._engine is not None:
      await self._engine.dispose()
      self._engine = None
      self._session_factory = None
      logger.info("Postgres连接关闭成功")
    get_postgres.cache_clear()

  @property
  def session_factory(self) -> async_sessionmaker[AsyncSession]:
    """只读属性，返回已经初始化的会话工厂"""
    if self._session_factory is None:
      raise RuntimeError("Postgres会话工厂未初始化，请先调用init()方法初始化")
    return self._session_factory


@lru_cache()
def get_postgres() -> Postgress:
  """获取Postgres单例实例"""
  return Postgress()


async def get_db_session() -> AsyncSession:
  """FastAPI依赖项，用于在每个请求中异步获取数据库会话实例，确保会话在正确使用后关闭"""

  # 获取引擎和会话工厂
  db = get_postgres()
  session_factory = db.session_factory

  # 创建会话上下文，在上下文内完成提交
  async with session_factory() as session:
    try:
      yield session
      await session.commit()
    except Exception as e:
      await session.rollback()
      raise e
    finally:
      await session.close()
