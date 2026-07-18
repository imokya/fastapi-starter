from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
  """项目基础设置，从.env或者环境变量中加载信息"""

  # 项目基础设置
  env: str = "development"
  log_level: str = "INFO"

  # 数据库相关配置
  sqlalchemy_database_url: str = ""

  # redis缓存配置
  redis_host: str = "localhost"
  redis_port: int = 6379
  redis_password: str | None = None
  redis_db: int = 0

  # 腾讯云COS配置
  cos_secret_id: str = ""
  cos_secret_key: str = ""
  cos_bucket_name: str = ""
  cos_region: str = ""
  cos_scheme: str = "https"
  cos_domain: str = ""

  # 使用pydantic完成环境变量信息加载
  model_config = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8",
    extra="ignore"
  )

  # jwt配置
  jwt_secret_key: str = ""
  jwt_algorithm: str = "HS256"
  jwt_expire_time: int = 604800


@lru_cache()
def get_settings() -> Settings:
  """获取项目配置信息，使用缓存，避免重复加载"""
  return Settings()
