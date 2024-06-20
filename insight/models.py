import datetime
from typing import List, Annotated
from sqlmodel import SQLModel, Field, Relationship

from user.models import User


class Insight(SQLModel, table=True):

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

    id: int| None = Field(default=None, primary_key=True)
    note: str
    likes: int | None
    date: str
    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="insight")
    reply: List["Reply"] = Relationship(back_populates="insight")


class Reply(SQLModel, table=True):

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

    id: int| None = Field(default=None, primary_key=True)
    text: str
    date: str
    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship()
    insight_id: int = Field(foreign_key="insight.id")
    insight: Insight = Relationship(back_populates="reply")
