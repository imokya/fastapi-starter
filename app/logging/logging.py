import sys
import logging
from app.config import get_settings


def setup_logging():
  """设置日志配置，涵盖日志等级，输出格式，输出渠道等"""
  # 获取项目配置
  settings = get_settings()

  # 获取根日志处理器
  root_logger = logging.getLogger()

  # 设置根日志等级
  log_level = getattr(logging, settings.log_level.upper())
  root_logger.setLevel(log_level)

  # 日志输出格式定义
  formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
  )

  # 控制台输出处理器
  console_handler = logging.StreamHandler(sys.stdout)
  console_handler.setFormatter(formatter)
  console_handler.setLevel(log_level)

  # 添加控制台输出处理器到根日志处理器
  root_logger.addHandler(console_handler)

  root_logger.info("日志系统初始化完成")
