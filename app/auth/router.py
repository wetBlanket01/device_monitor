# app/auth/router.py
from typing import Annotated

from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.schemas import SUserRegister, SUserAuth, SUserInfo
from app.users.models import User
from app.dao.dependencies import get_session_with_commit, get_session_without_commit
from app.auth.service import AuthService
from app.auth.dependencies import get_current_user, check_refresh_token

router = APIRouter()


@router.post(path='/register/')
async def register_user(
        user_data: SUserRegister,
        session: Annotated[AsyncSession, Depends(get_session_with_commit)]
):
    return await AuthService(session).register(user_data)


@router.post(path='/login/')
async def auth_user(
        response: Response,
        user_data: SUserAuth,
        session: Annotated[AsyncSession, Depends(get_session_without_commit)]
):
    return await AuthService(session).login(response, user_data)


@router.post(path='/logout/')
async def logout(response: Response):
    return AuthService.logout(response)


@router.get(path='/me/')
async def get_me(user_data: Annotated[User, Depends(get_current_user)]) -> SUserInfo:
    return SUserInfo.model_validate(user_data)


@router.post(path='/refresh/')
async def process_refresh_token(
        response: Response,
        user: Annotated[User, Depends(check_refresh_token)]
):
    return AuthService.refresh(response, user_id=user.id)