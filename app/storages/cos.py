import logging
from typing import Optional
from app.config import get_settings, Settings
from qcloud_cos import CosConfig, CosS3Client

from functools import lru_cache

logger = logging.getLogger(__name__)


class COS:
  """腾讯云COS存储"""

  def __init__(self):
    self._settings: Settings = get_settings()
    self._client: Optional[CosS3Client] = None

  async def init(self) -> None:
    """初始化腾讯云COS客户端"""

    # 判断客户端是否已经初始化，如果存在记录日志并返回
    if self._client is not None:
      logger.warning("腾讯云COS客户端已经初始化，无需重复初始化")
      return

    try:
      config = CosConfig(
        Region=self._settings.cos_region,
        SecretId=self._settings.cos_secret_id,
        SecretKey=self._settings.cos_secret_key,
        Scheme=self._settings.cos_scheme,
        Token=None,
      )
      self._client = CosS3Client(config)
      logger.info("腾讯云COS客户端初始化成功")
    except Exception as e:
      logger.error(f"初始化腾讯云COS客户端失败: {str(e)}")
      raise e

  async def shutdown(self) -> None:
    """关闭腾讯云COS客户端"""
    if self._client is not None:
      self._client = None
      logger.info("腾讯云COS客户端关闭成功")
      get_cos.cache_clear()
    else:
      logger.warning("腾讯云COS客户端未初始化，先调用init()方法初始化")

  @property
  def client(self) -> CosS3Client:
    """只读属性，返回已经初始化的客户端"""
    if self._client is None:
      raise RuntimeError("腾讯云COS客户端未初始化，请先调用init()方法初始化")
    return self._client


@lru_cache()
def get_cos() -> COS:
  """获取腾讯云COS实例"""
  return COS()
