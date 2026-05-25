from datetime import timezone, datetime
from typing import Annotated

import jwt
from jwt.exceptions import PyJWTError, ExpiredSignatureError
from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.dao.dependencies import get_session_without_commit
from app.users.dao import UserDAO
from app.users.models import User
from app.core.exceptions import TokenExpiredException, NoJWTException, NoUserIdException, UserNotFoundException, TokenNotFound


def get_access_token(request: Request) -> str:
    token = request.cookies.get("user_access_token")
    if not token:
        raise TokenNotFound
    return token


def get_refresh_token(request: Request) -> str:
    token = request.cookies.get("user_refresh_token")
    if not token:
        raise TokenNotFound
    return token


async def check_refresh_token(
        token: Annotated[str, Depends(get_refresh_token)],
        session: Annotated[AsyncSession, Depends(get_session_without_commit)]
) -> User:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        user_id = payload.get("sub")
        if not user_id:
            raise NoJWTException

        user = await UserDAO(session).find_one_or_none_by_id(data_id=user_id)
        if not user:
            raise NoJWTException

        return user
    except PyJWTError:
        raise NoJWTException


async def get_current_user(
        token: Annotated[str, Depends(get_access_token)],
        session: Annotated[AsyncSession, Depends(get_session_without_commit)]
) -> User:
    try:
        payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except ExpiredSignatureError:
        raise TokenExpiredException
    except PyJWTError:
        raise NoJWTException

    expire: str = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise TokenExpiredException

    user_id = payload.get('sub')
    if not user_id:
        raise NoUserIdException

    user = await UserDAO(session).find_one_or_none_by_id(data_id=user_id)
    if not user:
        raise UserNotFoundException

    return user
