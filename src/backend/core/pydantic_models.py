# coding: utf-8

from pydantic import BaseModel, EmailStr


class UserPost(BaseModel):
    username: str
    password: str
    email: EmailStr


class ReturnedUser(BaseModel):
    id: int
    username: str
    email: EmailStr


class UserLogin(BaseModel):
    username: str
    password: str


class UserInDB(BaseModel):
    id: int
    username: str
    email: EmailStr
    # avatar_path: str
    # permissions:
