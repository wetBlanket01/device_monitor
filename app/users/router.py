from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.dependencies import get_session_without_commit
from app.auth.dependencies import get_current_user
from app.users.service import UserStatsService
from app.users.models import User

router = APIRouter()


@router.get('/me/stats/')
async def get_aggregated_stats(
        user: Annotated[User, Depends(get_current_user)],
        session: Annotated[AsyncSession, Depends(get_session_without_commit)]
):
    return await UserStatsService(session).start_aggregated_stats(user.id)


@router.get('/me/stats/each/')
async def get_stats_each_device(
        user: Annotated[User, Depends(get_current_user)],
        session: Annotated[AsyncSession, Depends(get_session_without_commit)]
):
    return await UserStatsService(session).start_stats_each_device(user.id)
