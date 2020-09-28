# coding: utf-8
import hashlib

from fastapi import Security, HTTPException, status, Depends
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader

from sqlalchemy import select
from sqlalchemy.sql import bindparam

from backend.core.pydantic_models import UserInDB
from backend.core.setting import get_setting, redisDBenum
from backend.db.connector import db, get_redis
from backend.db.models.user import user

access_token_query = APIKeyQuery(name="access_token", auto_error=False)
access_token_header = APIKeyHeader(name="access_token", auto_error=False)
access_token_cookie = APIKeyCookie(name="access_token", auto_error=False)


def hash_password(password: str) -> str:
    temp_hash = password
    for _ in range(10000):
        temp_hash = hashlib.sha512(temp_hash.encode("utf-8")).hexdigest()
    return temp_hash


async def get_access_token(
    access_token_query: str = Security(access_token_query),
    access_token_header: str = Security(access_token_header),
    access_token_cookie: str = Security(access_token_cookie),
):
    if access_token_query is not None:
        return access_token_query

    elif access_token_header is not None:
        return access_token_header

    elif access_token_cookie is not None:
        return access_token_cookie

    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="access-token is missing"
        )


async def get_current_user(
    access_token: str = Depends(get_access_token),
    setting=Depends(get_setting),
    redis=Depends(get_redis(redisDBenum.session.value)),
):
    user_id = await redis.get(access_token)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    user_id = int(user_id)  # cast in int because redis stock int as bytes
    query = str(
        select([user.c.username, user.c.email]).where(user.c.id == bindparam("user_id"))
    )
    result = await db.fetch_one(query=query, values={"user_id": user_id})
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    await redis.expire(access_token, setting.session_ttl)
    username, email = result.values()
    return UserInDB(id=user_id, username=username, email=email)
