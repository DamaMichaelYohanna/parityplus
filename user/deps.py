from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from sqlmodel import select

from database import get_session
from user.models import User
from user.schemas import TokenPayLoad
from user.utility import (
    ALGORITHM,
    JWT_SECRET_KEY
)

from jose import jwt


reusable_oauth = OAuth2PasswordBearer(
    tokenUrl="/user/login",
    scheme_name="JWT"
)


def get_current_user(
        token: str = Depends(reusable_oauth),
        session=Depends(get_session)
):
    try:
        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = TokenPayLoad(**payload)
        print(payload, token_data)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user: User = session.exec(select(User).where(User.username==token_data.user)).one()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return user
