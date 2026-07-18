from enum import Enum
from pydantic import BaseModel, Field
from typing import Generic, TypeVar, Optional


T = TypeVar('T')


class HttpCode(int, Enum):
  SUCCESS = 200
  BAD_REQUEST = 400
  UNAUTHORIZED = 401
  FORBIDDEN = 403
  NOT_FOUND = 404
  VALIDATION_ERROR = 422
  TOO_MANY_REQUESTS = 429
  INTERNAL_SERVER_ERROR = 500


class Response(BaseModel, Generic[T]):
  """基础API响应结构，继承BaseModel，并定义泛型"""
  code: int = HttpCode.SUCCESS
  msg: str = 'success'
  data: Optional[T] = Field(default_factory=dict)  # 响应数据默认为空字典

  @staticmethod
  def success(msg: str = 'success', data: Optional[T] = None) -> 'Response[T]':
    """成功消息，传递msg+data，code固定为200"""
    if data is None:
      return Response(code=HttpCode.SUCCESS, msg=msg)
    return Response(code=HttpCode.SUCCESS, msg=msg, data=data)

  @staticmethod
  def fail(code: HttpCode, msg: str, data: Optional[T] = None) -> 'Response[T]':
    """失败消息，传递code+msg+data"""
    if data is None:
      return Response(code=code, msg=msg)
    return Response(code=code, msg=msg, data=data)
