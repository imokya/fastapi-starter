import logging
from app.utils import Response
from app.utils.response import HttpCode
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException
from .exceptions import AppException

logger = logging.getLogger(__name__)

FIELD_LABELS = {
  "username": "用户名",
  "password": "密码",
}


def register_exception_handlers(app: FastAPI):
  """处理项目中所有异常并进行统一处理，涵盖：自定义业务异常，HTTP异常，通用异常"""

  @app.exception_handler(RequestValidationError)
  async def request_validation_handler(request: Request, e: RequestValidationError):
    """处理 FastAPI/Pydantic 请求参数验证错误"""
    print('==========', )
    return JSONResponse(
      status_code=HttpCode.VALIDATION_ERROR.value,
      content=Response(
        code=HttpCode.VALIDATION_ERROR,
        msg=e.errors()[0].get('msg'),
        data={},
      ).model_dump(),
    )

  @app.exception_handler(AppException)
  async def app_exception_handler(request: Request, e: AppException):
    """处理自定义业务异常，将状态吗统一设置为400"""
    logger.error(f"AppException: {e.msg}")
    return JSONResponse(
      status_code=e.status_code,
      content=Response(
        code=e.status_code,
        msg=e.msg,
        data={}
      ).model_dump()
    )

  @app.exception_handler(HTTPException)
  async def http_exception_handler(request: Request, e: HTTPException):
    """处理HTTP异常，将所有状态统一响应结构"""
    logger.error(f"HTTPException: {e.detail}")
    return JSONResponse(
      status_code=e.status_code,
      content=Response(
        code=e.status_code,
        msg=e.detail,
        data={}
      ).model_dump()
    )

  @app.exception_handler(Exception)
  async def exception_handler(request: Request, e: Exception):
    """处理项目抛出的未定义的任意异常，将状态吗统一设置为500"""
    logger.error(f"Exception: {str(e)}")
    return JSONResponse(
      status_code=500,
      content=Response(
        code=500,
        msg="服务器出现异常，请稍后重试",
        data={}
      ).model_dump()
    )
