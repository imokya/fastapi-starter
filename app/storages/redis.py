import logging
from redis.asyncio import Redis
from app.config import get_settings, Settings
from functools import lru_cache

logger = logging.getLogger(__name__)


class RedisClient:
  """Redis客户端，用于完成redis缓存连接和使用"""

  def __init__(self):
    """构造函数，完成redis客户端初始化"""
    self._client: Redis | None = None
    self._settings: Settings = get_settings()

  async def init(self) -> None:
    """完成redis客户端初始化"""
    # 判断客户端是否存在，如果存在则表示已经连上，无需重复连接
    if self._client:
      logger.warning("Redis客户端已经初始化，无需重复连接")
      return

    try:
      # 创建redis客户端
      self._client = Redis(
        db=self._settings.redis_db,
        host=self._settings.redis_host,
        port=self._settings.redis_port,
        password=self._settings.redis_password,
        decode_responses=True
      )

      # 测试连接
      await self._client.ping()
      logger.info("Redis客户端初始化成功")
    except Exception as e:
      logger.error(f"Redis客户端初始化失败: {str(e)}")
      raise e

  async def shutdown(self) -> None:
    """关闭redis客户端"""
    if self._client is not None:
      await self._client.close()
      self._client = None
      logger.info("Redis客户端关闭成功")

    # 清理缓存
    get_redis.cache_clear()

  @property
  # 只读属性返回redis客户端
  def client(self) -> Redis:
    """获取redis客户端"""
    if self._client is None:
      raise RuntimeError("Redis客户端未初始化，获取客户端失败")
    return self._client


@lru_cache()
def get_redis() -> RedisClient:
  """获取redis客户端"""
  return RedisClient()
