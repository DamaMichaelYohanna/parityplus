from sqlmodel import SQLModel, Field, Relationship

from user.models import User


class Job(SQLModel, table=True):
    """Database table for keeping records of jobs"""
    class Config:
        from_attributes = True

    id: int | None = Field(default=None, primary_key=True)
    title: str
    details: str
    filter: str
    author_id: int = Field(foreign_key="user.id")
    # user: User = Relationship(back_populates="job")
    date: str
