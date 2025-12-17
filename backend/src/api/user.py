from typing import Any

from fastapi import APIRouter, Query
from fastapi.params import Depends

from backend.src.dependencies import (CurrentUser,
                                      get_current_admin,
                                      user_serviceDP)
from backend.src.models.user import (UserCreate,
                                     UserResponse,
                                     UserUpdate)

router = APIRouter(prefix="/users", tags=["Пользователи"])

@router.get("",
            dependencies=[Depends(get_current_admin)],
            response_model=list[UserResponse],
            description="Получение списка всех пользователей",
            summary="Get ALL the user's list")
async def get_all_users(
        current_user: CurrentUser,
        user_service: user_serviceDP,
        offset: int = 0,
        limit: int = Query(default=50, le=500),
) -> Any:
    return await user_service.get_users(offset=offset, limit=limit)


@router.get("/{user_id}",
            dependencies=[Depends(get_current_admin)],
            response_model=UserResponse,
            description="Получение записи о пользователе по ID",
            summary="Get user by ID")
async def get_one_user(user_service: user_serviceDP, user_id: int) -> Any:
    return await user_service.get_user(user_id)



@router.post("/",
             dependencies=[Depends(get_current_admin)],
             response_model=UserResponse,
             description="Добавление записи о пользователе АДМИНОМ",
             summary="Add user by ADMIN")
async def user_create(user_service: user_serviceDP, user_data: UserCreate) -> UserResponse:
    return await user_service.create_user(user_data)


@router.patch("/{user_id}",
              dependencies=[Depends(get_current_admin)],
              response_model=UserResponse,
              description="Обновление записи о пользователе по ID",
              summary="Update user by ID")
async def update_user(
    user_service: user_serviceDP, user_id: int, user_data: UserUpdate
) -> Any:
    return await user_service.part_update_user(user_id, user_data)


@router.delete("/{user_id}",
               dependencies=[Depends(get_current_admin)],
               description="Удаление записи о пользователе по ID",
               summary="Delete user by ADMIN")
async def del_user(user_service: user_serviceDP, user_id: int) -> bool:
    return await user_service.del_user(user_id)
