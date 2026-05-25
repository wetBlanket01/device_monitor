from fastapi import Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException
from app.users.schemas import SUserRegister, SUserAddDB, SUserAuth
from app.users.dao import UserDAO
from app.auth.utils import authenticate_user, set_tokens


class AuthService:
    def __init__(self, session: AsyncSession):
        self.user_dao = UserDAO(session)

    async def register(self, user_data: SUserRegister) -> dict:
        existing_user = await self.user_dao.find_one_or_none(
            filters_dict={'username': user_data.username}
        )
        if existing_user:
            raise UserAlreadyExistsException

        user_data_dict = user_data.model_dump()
        user_data_dict.pop('confirm_password', None)
        user_data_dict['password_hash'] = user_data_dict.pop('password')

        await self.user_dao.add(values=SUserAddDB(**user_data_dict))
        return {'message': 'User created successfully'}

    async def login(self, response: Response, user_data: SUserAuth) -> dict:
        user = await self.user_dao.find_one_or_none(
            filters_dict={'username': user_data.username}
        )
        if not (user and authenticate_user(user=user, password=user_data.password)):
            raise IncorrectEmailOrPasswordException

        set_tokens(response, user_id=user.id)
        return {'ok': True, 'message': 'Authentication successful'}

    @staticmethod
    def logout(response: Response) -> dict:
        response.delete_cookie('user_access_token')
        response.delete_cookie('user_refresh_token')
        return {'message': 'Logged out successfully'}

    @staticmethod
    def refresh(response: Response, user_id: str) -> dict:
        set_tokens(response, user_id=user_id)
        return {'message': 'Tokens refresh successful'}
