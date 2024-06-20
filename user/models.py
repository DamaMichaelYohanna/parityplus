from enum import Enum as PyEnum

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlmodel import SQLModel, Session, Field, Relationship, select
from typing import List
from database import get_session


# Define the Enum for Status
class Status(PyEnum):
    FOLLOWING = 1
    BLOCKED = 0


class Associate(SQLModel, table=True):
    class Config:
        from_attributes = True

    by_id: int = Field(foreign_key='user.id', primary_key=True, description='Relationship from')
    to_id: int = Field(foreign_key='user.id', primary_key=True, description='Relationship to')
    status: int | None = None

    # Define the Many-to-Many relationship
    by: "User" = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "Associate.by_id==User.id", })
    to: "User" = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "Associate.to_id==User.id", }
    )

    def get_or_create(self, user_id):
        with get_session() as session:
            filter_statement = select(Associate).where(
                Associate.by == self,
                Associate.to == user_id
            )
            associate = session.exec(filter_statement)
            if associate:
                return associate
            else:
                associate = Associate(by=self, to=user_id)
                session.add(associate)
                session.commit()
                return associate


class User(SQLModel, table=True):
    class Config:
        from_attributes = True

    id: int | None = Field(default=None, primary_key=True)
    username: str
    password: str
    full_name: str | None = None
    email: str | None = None
    gender: str | None = None
    picture: bytes | None = None
    cover: bytes | None = None
    bio: str | None = None
    phone: int | None = None
    address: str | None = None
    email_verified: bool | None = None

    follow: List["Associate"] = Relationship(
        back_populates="by",
        sa_relationship_kwargs={
            "primaryjoin": "Associate.by_id==User.id"}
    )
    insight: List["Insight"] = Relationship(back_populates="user")

    def get_following(self, session: Session):
        """return the people the current user is following"""
        filter_statement = select(Associate).where(Associate.by == self)
        following = session.exec(filter_statement)
        return following.all()

    def get_followers(self, session: Session):
        """return the user that are currently following the user"""
        filter_statement = select(Associate).where(Associate.to == self)
        followers = session.exec(filter_statement)
        return followers.all()

    def follow_user(self, session: Session, user_2_follower):
        associate: Associate = Associate(by=self, to=user_2_follower, status=1)
        session.add(associate)
        try:
            session.commit()
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Can't not follow same user twice",
            )

    def unfollow_user(self, session: Session, user_2_unfollower):
        filter_statement = select(Associate).where(
            Associate.by == self,
            Associate.to == user_2_unfollower,
            Associate.status == 1

        )
        try:
            return_value = session.exec(filter_statement).one()
            session.delete(return_value)
            session.commit()
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No association",
            )

    def block_user(self, session: Session, user_2_block):
        filter_statement: select = select(Associate).where(
            Associate.by == self,
            Associate.to == user_2_block,
        )
        return_value = session.exec(filter_statement).first()
        if return_value:
            return_value.status = 0
        else:
            associate: Associate = Associate(
                by=self,
                to=user_2_block,
                status=0
            )
            session.add(associate)
            session.commit()

    def unblock_user(self, session: Session, user_2_unblock):
        filter_statement = select(Associate).where(
            Associate.by == self,
            Associate.to == user_2_unblock,

        )
        return_value = session.exec(filter_statement).first()
        if return_value:
            session.delete(return_value)
            session.commit()
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No association. Can not unblock",
            )


