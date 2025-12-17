import jwt
from sqladmin.authentication import AuthenticationBackend
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col
from starlette.requests import Request
from starlette.exceptions import HTTPException
from jwt.exceptions import ExpiredSignatureError
from starlette.responses import RedirectResponse

from backend.src.admin.dependency import session_maker_admin
from backend.src.config import settings

from backend.src.models.user import User
from backend.src.security import verify_password, create_access_token


async def authenticate_admin(
    db: AsyncSession,
    email: str,
    password: str,
):
    stmt = select(User).where(User.email == email)
    res = await db.execute(stmt)
    user = res.scalar_one_or_none()

    if user:
        if user.is_admin:
            valid_password = verify_password(password, user.hashed_password)
            if valid_password:
                return user
            else:
                return False
        else:
            raise HTTPException(status_code=403, detail="Доступ запрещен")


class AdminAuth(AuthenticationBackend):
    def __init__(self, secret_key: str):
        super().__init__(secret_key)
        self.redirect_url = "http://localhost:8000/admin/login"  # TODO: change domain

    async def login(
        self,
        request: Request,
    ) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]

        async with session_maker_admin() as db:
            try:
                user = await authenticate_admin(db, email, password)
            except AttributeError:
                return False

            if user:
                token = create_access_token({"sub": user.email})
                request.session.update({"token": token})
                return True

            return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def check_token_exp(self, token: str, request: Request) -> RedirectResponse:
        if token:
            try:
                jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            except ExpiredSignatureError:
                await self.logout(request)
                return RedirectResponse(self.redirect_url, status_code=303)

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        await self.check_token_exp(token, request)

        if not token:
            return False
        return True
