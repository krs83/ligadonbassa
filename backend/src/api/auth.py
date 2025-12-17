from typing import Annotated, Any

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from backend.src.dependencies import (CurrentUser,
                                      auth_serviceDP,
                                      user_serviceDP)
from backend.src.models.token import Token
from backend.src.models.user import (UserLogin,
                                     UserResponse,
                                     UserCreate, User)

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])



@router.post("/login/access_token",
             response_model=Token,
             description="Получение токена по форме",
             summary="Get access token by email&password")
async def login_user(
    auth_service: auth_serviceDP,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user_data = UserLogin(email=form_data.username, password=form_data.password)
    return await auth_service.login_access_token(user_data)


@router.post("/signup",
             response_model=UserResponse,
             description="Регистрация пользователя без аутентификации",
             summary="Register user by email&password")
async def register_user(user_service: user_serviceDP, user_data: UserLogin) -> UserResponse:
    _user_create = UserCreate.model_validate(user_data)
    return await user_service.create_user(user_data)


@router.get("/me",
            response_model=UserResponse,
            description="Получение данных о текущем пользователе",
            summary="Get current user")
async def get_me(current_user: CurrentUser) -> User:
    return current_user
