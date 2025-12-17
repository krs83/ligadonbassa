from typing import Any

from pydantic import EmailStr
from backend.src.models import User
from backend.src.repositories.base import BaseRepository


class UserRepository(BaseRepository):

    async def get_users(self, offset: int, limit: int) -> list[User]:
        return await self._get_many(model=User, offset=offset, limit=limit)

    async def get_user_by_id(self, user_id: int) -> User:
        return await self._get_pk(model=User, pk=user_id)

    async def get_user_by_email(self, user_email: EmailStr) -> User:
        return await self._get_one(User, User.email == user_email)

    async def create_user(self, db_user: User) -> User:
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return db_user

    async def update_user(
        self, user_id: int, user_data: dict[str, Any], extra_data: dict[str, Any]
    ) -> User:
        db_user = await self._update(User, user_data, user_id, extra=extra_data)
        await self.session.commit()
        await self.session.refresh(db_user)
        return db_user

    async def delete_user(self, user_id: int) -> bool:
        result = await self._delete(User, User.id == user_id)
        await self.session.commit()
        return result
