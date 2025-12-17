import asyncio

from sqlmodel.ext.asyncio.session import AsyncSession

from backend.src.config import settings
from backend.src.database import engine
from backend.src.models.user import User
from backend.src.security import hash_password


async def create_admin():
    email = settings.ADMIN_LOGIN
    password = settings.ADMIN_PASSWORD

    if not email or not password:
        print("email или password не указаны")
        return

    async with AsyncSession(engine) as session:
        hashed_password = hash_password(password)

        admin = {
            "email": email,
            "is_admin": True
        }

        extra_data = {"hashed_password": hashed_password}
        admin_data = User.model_validate(admin, update=extra_data)


        session.add(admin_data)
        await session.commit()
        print(f"✅ Админ создан: {email}")

if __name__ == "__main__":
    asyncio.run(create_admin())