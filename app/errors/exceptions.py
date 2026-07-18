

from typing import Any
from app.utils.response import HttpCode


class AppException(RuntimeError):
  """基础应用异常类，继承RuntimeError"""

  def __init__(
    self,
    code: int = HttpCode.BAD_REQUEST.value,
    status_code: int = HttpCode.BAD_REQUEST.value,
    msg: str = '应用发生错误，请稍后尝试',
    data: Any = None
  ):
    """构造函数，完成错误数据初始化"""
    self.msg = msg
    self.code = code
    self.data = data
    self.status_code = status_code
    super().__init__()


class BadRequestError(AppException):
  """客户端请求错误"""

  def __init__(self, msg: str = '客户端请求错误，请检查后重试'):
    super().__init__(
      status_code=HttpCode.BAD_REQUEST.value,
      code=HttpCode.BAD_REQUEST.value,
      msg=msg
    )


class NotFoundError(AppException):
  """资源未找到错误请求"""

  def __init__(self, msg: str = '资源未找到，请检查后重试'):
    super().__init__(
      status_code=HttpCode.NOT_FOUND.value,
      code=HttpCode.NOT_FOUND.value,
      msg=msg
    )


class ValidationError(AppException):
  """数据验证错误"""

  def __init__(self, msg: str = '数据验证错误，请检查后重试'):
    super().__init__(
      status_code=HttpCode.VALIDATION_ERROR.value,
      code=HttpCode.VALIDATION_ERROR.value,
      msg=msg
    )


class UnauthorizedError(AppException):
  """未授权错误"""

  def __init__(self, msg: str = '未授权，请重新登录'):
    super().__init__(
      status_code=HttpCode.UNAUTHORIZED.value,
      code=HttpCode.UNAUTHORIZED.value,
      msg=msg
    )


class TooManyRequestsError(AppException):
  """请求过多错误"""

  def __init__(self, msg: str = '请求过多，请稍后重试'):
    super().__init__(
      status_code=HttpCode.TOO_MANY_REQUESTS.value,
      code=HttpCode.TOO_MANY_REQUESTS.value,
      msg=msg
    )


class ServerError(AppException):
  """服务器错误"""

  def __init__(self, msg: str = '服务器错误，请稍后重试'):
    super().__init__(
      status_code=HttpCode.INTERNAL_SERVER_ERROR.value,
      code=HttpCode.INTERNAL_SERVER_ERROR.value,
      msg=msg
    )
