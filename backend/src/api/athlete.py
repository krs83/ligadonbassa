from typing import List

from fastapi import APIRouter, Query, Depends, Body

from backend.src.dependencies import athlete_serviceDP, get_current_admin
from backend.src.models.athlete import (
    AthleteCreate,
    AthleteResponse,
    AthleteBase,
    AthleteUpdate,
    Athlete,
)

router = APIRouter(prefix="/athletes", tags=["Спортсмены"])


@router.get("",
            response_model=list[AthleteResponse],
            description="Получение списка всех спортсменов",
            summary="Get athletes list")
async def get_all_athletes(
    athlete_service: athlete_serviceDP,
    offset: int = Query(default=0, ge=0, description="Смещение для пагинации"),
    limit: int = Query(default=50, le=500, description="Лимит записей на страницу"),
) -> list[Athlete]:
    return await athlete_service.get_athletes(offset, limit)


@router.get("/admin",
            dependencies=[Depends(get_current_admin)],
            response_model=list[AthleteResponse],
            description="Получение списка всех спортсменов, включая неактивных",
            summary="Get all athletes list including not active")
async def admin_get_all_athletes(
        athlete_service: athlete_serviceDP,
        offset: int = Query(default=0, ge=0, description="Смещение для пагинации"),
        limit: int = Query(default=50, le=500, description="Лимит записей на страницу"),
) -> list[Athlete]:
    return await athlete_service.admin_get_athletes(offset, limit)


@router.get("/id/{athlete_id}",
            response_model=AthleteResponse,
            description="Получение спортсмена по ID",
            summary="Get athlete by ID")
async def get_one_athlete(
    athlete_service: athlete_serviceDP, athlete_id: int
) -> AthleteBase:
    return await athlete_service.get_athlete(athlete_id)

@router.get("/admin/id/{athlete_id}",
            dependencies=[Depends(get_current_admin)],
            response_model=AthleteResponse,
            description="Получение спортсмена по ID, включая неактивного",
            summary="Get athlete by ID including not active")
async def admin_get_one_athlete(
        athlete_service: athlete_serviceDP, athlete_id: int
) -> AthleteBase:
    return await athlete_service.admin_get_athlete(athlete_id)

@router.get("/search/{athlete_data}",
            response_model=List[AthleteResponse],
            description="Поиск спортсмена по имени",
            summary="Search athlete by name")
async def search_athlete_by_name(
        athlete_service: athlete_serviceDP, athlete_data: str
) -> AthleteBase:
    return await athlete_service.search_athlete_by_name(athlete_data)


@router.post("",
             dependencies=[Depends(get_current_admin)],
             response_model=AthleteResponse,
             description="Добавление записи о спортсмене в БД",
             summary="Add athlete to DB")
async def add_athlete(
    athlete_service: athlete_serviceDP, athlete_data: AthleteCreate
) -> AthleteBase:
    return await athlete_service.create_athlete(athlete_data)


@router.post("/bulk-create",
             dependencies=[Depends(get_current_admin)],
             response_model=List[AthleteResponse],
             description="Добавление списка записей о спортсменах в БД",
             summary="Add athletes list to DB")
async def add_few_athletes(
        athlete_service: athlete_serviceDP, athlete_data: List[AthleteCreate]
) -> List[AthleteResponse]:
    return await athlete_service.create_few_athletes(athlete_data)

@router.patch("/bulk-update",
              dependencies=[Depends(get_current_admin)],
              response_model=list[AthleteResponse],
              description="Массовое обновление данных о спортсменах по ID",
              summary="Bulk athletes updates by ID")
async def bulk_update_athletes(
        athlete_service: athlete_serviceDP,
        athletes_id: list[int] = Query(),
        athlete_data: AthleteUpdate = Body()
) -> List[AthleteResponse]:
    return await athlete_service.bulk_update_athletes(athletes_id, athlete_data)


@router.delete("/{athlete_id}",
               dependencies=[Depends(get_current_admin)],
               description="Мягкое удаление записи о спортсмене из БД по ID",
               summary="Soft delete athlete by ID")
async def soft_del_athlete(athlete_service: athlete_serviceDP, athlete_id: int) -> dict:
    return await athlete_service.soft_del_athlete(athlete_id)


@router.patch("/restore/{athlete_id}",
               dependencies=[Depends(get_current_admin)],
               description="Восстановление записи о спортсмене в БД по ID",
               summary="Restore athlete by ID")
async def restore_athlete(athlete_service: athlete_serviceDP, athlete_id: int) -> dict:
    return await athlete_service.restoring_athlete(athlete_id)

@router.patch("/{athlete_id}",
              dependencies=[Depends(get_current_admin)],
              response_model=AthleteResponse,
              description="Обновление данных о спортсмене по ID",
              summary="Update athlete by ID")
async def update_athlete(
        athlete_service: athlete_serviceDP, athlete_id: int, athlete_data: AthleteUpdate
) -> AthleteBase:
    return await athlete_service.part_update_athlete(athlete_id, athlete_data)

