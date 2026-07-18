from pydantic import BaseModel, Field, field_validator, ConfigDict


class CreateUserReq(BaseModel):
  username: str = Field(..., description="用户名", title="用户名")
  password: str = Field(..., description="密码", title="密码")

  @field_validator('username')
  @classmethod
  def validate_username(cls, value: str) -> str:
    if not value:
      raise ValueError('用户名不能为空')
    return value

  @field_validator('password')
  @classmethod
  def validate_password(cls, value: str) -> str:
    if not value:
      raise ValueError('密码不能为空')
    return value
