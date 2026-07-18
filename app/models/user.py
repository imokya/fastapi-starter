import uuid
from .base import Base
from datetime import datetime
from sqlalchemy import (
  UUID,
  String,
  text,
  DateTime,
  PrimaryKeyConstraint
)
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
  __tablename__ = "users"
  __table_args__ = (
    PrimaryKeyConstraint("id", name="uq_id"),
  )

  id: Mapped[uuid.UUID] = mapped_column(
    UUID, primary_key=True, nullable=False, server_default=text("uuid_generate_v4()"))
  username: Mapped[str] = mapped_column(
    String(255), nullable=False, server_default=text("''::character varying"))
  password: Mapped[str] = mapped_column(
    String(255), nullable=False, server_default=text("''::character varying"))
  email: Mapped[str] = mapped_column(String(255), default="")
  openid: Mapped[str] = mapped_column(String(255), default="")
  created_at: Mapped[datetime] = mapped_column(
    DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP(0)"))
  updated_at: Mapped[datetime] = mapped_column(
    DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP(0)"),)
