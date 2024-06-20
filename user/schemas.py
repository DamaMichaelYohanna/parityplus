from datetime import datetime
from typing import List

from pydantic import BaseModel
from sqlmodel import SQLModel, Relationship


class RegisterInSchema(SQLModel):
    """Schema for receiving user credentials"""
    username: str
    password: str
    email: str
    gender: str
    full_name: str


class RegisterOutSchema(SQLModel):
    """Schema to output user info after registration"""
    id: int
    username: str
    email: str | None = None


class Associate(BaseModel):
    """model to query association"""
    followers: List["User"]| int| None = None
    following: List["User"]| int | None = None


class User(SQLModel):
    """model to query only user detail"""
    username: str | None = None
    full_name: str | None = None
    email: str | None = None
    gender: str | None = None
    bio: str | None = None
    cover: str | None = None
    picture: str | None = None
    phone: str | None = None


class Profile(SQLModel):
    """model to combine user and their followers"""
    user: User
    associate: Associate
    owner: bool = False


class TokenPayLoad(SQLModel):
    exp: int
    user: str
