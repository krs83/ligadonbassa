from pydantic import EmailStr

from backend.src.exceptions.auth import AuthFailedException
from backend.src.exceptions.user import UserEmailNotFoundException
from backend.src.models.token import Token
from backend.src.models.user import UserLogin, User
from backend.src.security import verify_password, create_access_token
from backend.src.services.base import BaseService


class AuthService(BaseService):
    async def authenticate_user(self, user_email: EmailStr, password: str) -> User:
        """Проверка на аутентификацию пользователя - email и пароль"""

        user = await self.repository.users.get_user_by_email(user_email)
        if not user:
            self.logger.error(UserEmailNotFoundException.USER_EMAIL_NOT_FOUND_TEXT.format(user_email))
            raise UserEmailNotFoundException(user_email)
        self.logger.info(f"Пользователь {user_email} успешно найден")
        if not verify_password(password, user.hashed_password):
            self.logger.error(AuthFailedException.AUTH_FAILED_TEXT)
            raise AuthFailedException()
        self.logger.info(f"Пользователь {user_email} успешно аутентифицирован")
        return user

    async def login_access_token(self, user_data: UserLogin) -> Token:
        """Получение токена при успешном входе"""

        user = await self.authenticate_user(user_data.email, user_data.password)

        data = {"sub": user.email, "is_admin": user.is_admin}
        access_token = create_access_token(data=data)
        return Token(access_token=access_token)

