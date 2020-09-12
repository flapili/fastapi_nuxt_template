# coding: utf-8
import sqlalchemy
from sqlalchemy.sql import func

from ..metadata import metadata


user = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, index=True,),
    sqlalchemy.Column(
        "username",
        sqlalchemy.String(length=64),
        index=True,
        nullable=False,
        unique=True,
    ),
    sqlalchemy.Column(
        "hashed_password", sqlalchemy.String(length=128), nullable=False,
    ),
    sqlalchemy.Column(
        "email", sqlalchemy.String(length=255), index=True, nullable=False, unique=True,
    ),
    sqlalchemy.Column(
        "created_at", sqlalchemy.DateTime, nullable=False, server_default=func.now(),
    ),
    sqlalchemy.Column(
        "updated_at",
        sqlalchemy.DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    ),
)
