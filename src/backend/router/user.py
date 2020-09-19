# coding: utf-8
import secrets

from fastapi import APIRouter, status, HTTPException, Response, Depends
from fastapi.responses import JSONResponse

import asyncpg.exceptions

from sqlalchemy import select
from sqlalchemy.sql import bindparam

from backend.core.auth import hash_password, get_user
from backend.core.pydantic_models import ReturnedUser, UserLogin, UserPost, UserInDB
from backend.db.connector import get_db
from backend.db.models.user import user
from backend.db.models.session import session


router = APIRouter()


@router.post(
    "",
    response_model=ReturnedUser,
    status_code=201,
    responses={409: {"description": "Username or email already used"}},
)
async def user_post(new_user: UserPost, db=Depends(get_db)):
    values = new_user.dict()

    values["hashed_password"] = hash_password(new_user.password)
    del values["password"]
    try:
        values["id"] = await db.execute(user.insert(), values=values)
        del values["hashed_password"]
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=values)
    except asyncpg.exceptions.UniqueViolationError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username or email already used",
        )


@router.post("/login")
async def login_user(
    response: Response, login_user: UserLogin, db=Depends(get_db), status_code=200
):
    query = str(
        select([user.c.id])
        .where(user.c.username == bindparam("username"))
        .where(user.c.hashed_password == bindparam("hashed_password"))
    )
    result = await db.fetch_one(
        query,
        values={
            "username": login_user.username,
            "hashed_password": hash_password(login_user.password),
        },
    )

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="wrong username or password",
        )

    user_id, *_ = result.values()
    token = secrets.token_urlsafe(128)[:64]

    await db.execute(session.insert(), values={"user_id": user_id, "token": token})
    response.set_cookie(key="access_token", value=token)
    return


@router.get("/me", response_model=UserInDB)
async def me(user=Depends(get_user)):
    return user
