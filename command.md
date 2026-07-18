# alembic创建数据表

alembic revision --autogenerate -m "create users table"

## 升级数据库到最新版本

alembic upgrade head

## 回退到上一个版本

alembic downgrade -1
