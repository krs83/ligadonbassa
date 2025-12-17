from sqlalchemy.exc import IntegrityError

from backend.src.exceptions.user import UserIDNotFoundException, UserConflictException
from backend.src.models.user import (
    UserCreate,
    User,
    UserResponse,
    UserUpdate,
    UserLogin,
)
from backend.src.security import hash_password
from backend.src.services.base import BaseService


class UserService(BaseService):

    async def get_users(self, offset: int, limit: int) -> list[User]:
        """Получение всех пользователей из БД согласно выборке"""
        self.logger.info("Получен список всех пользователей из БД согласно выборке")

        return await self.repository.users.get_users(offset=offset, limit=limit)

    async def get_user(self, user_id: int) -> User:
        """Получение конкретного пользователя по ID"""

        user =  await self.repository.users.get_user_by_id(user_id)
        if not user:
            self.logger.error(UserIDNotFoundException.USER_ID_NOT_FOUND_TEXT.format(user_id))
            raise UserIDNotFoundException(user_id)
        self.logger.info(f"Пользователь с ID №{user_id} успешно получен")
        return user

    async def create_user(
        self,
        user_data: UserCreate | UserLogin,
    ) -> UserResponse:
        """Добавление записи в БД о новом пользователе"""

        try:
            hashed_password = hash_password(user_data.password)
            extra_data = {"hashed_password": hashed_password}

            db_user = User.model_validate(user_data, update=extra_data)

            await self.repository.users.create_user(db_user)
        except IntegrityError:
            self.logger.error(UserConflictException.USER_CONFLICT_TEXT.format(user_data.email))
            raise UserConflictException(user_data.email)
        self.logger.info(f"Добавлен новый пользователь с email {user_data.email}")

        return UserResponse.model_validate(db_user)

    async def part_update_user(
        self,
        user_id: int,
        user_data: UserUpdate,
    ) -> UserResponse:
        """Частичное или полное обновление данных о пользователе по его ID"""

        try:
            user = user_data.model_dump(exclude_unset=True)
            extra_data = {}
            if "password" in user:
                password = user["password"]
                hashed_password = hash_password(password)
                extra_data["hashed_password"] = hashed_password
            db_user = await self.repository.users.update_user(
                user_id=user_id, user_data=user, extra_data=extra_data
            )
        except IntegrityError:
            self.logger.error(UserConflictException.USER_CONFLICT_TEXT.format(user_data.email))
            raise UserConflictException(user_data.email)
        if not db_user:
            self.logger.error(UserIDNotFoundException.USER_ID_NOT_FOUND_TEXT.format(user_id))
            raise UserIDNotFoundException(user_id)
        self.logger.info(f"Пользователь с ID №{user_id} успешно обновлён")

        return UserResponse.model_validate(db_user)

    async def del_user(self, user_id: int) -> bool:
        """Удаление записи о пользователе из БД по его ID"""

        user =  await self.repository.users.delete_user(user_id)
        if not user:
            self.logger.error(UserIDNotFoundException.USER_ID_NOT_FOUND_TEXT.format(user_id))
            raise UserIDNotFoundException(user_id)
        self.logger.info(f"Пользователь с ID №{user_id} успешно удалён")

        return user
