from fastapi import APIRouter, Query, Depends

from backend.src.dependencies import tournament_serviceDP, get_current_admin
from backend.src.models.tournament import (TournamentResponse,
                                           TournamentBase,
                                           TournamentAdd,
                                           TournamentUpdate,
                                            Tournament)

router = APIRouter(prefix="/tournaments", tags=["Турниры"])


@router.get("",
            response_model=list[TournamentResponse],
            description="Получение списка всех турниров",
            summary="Get tournaments list")
async def get_all_tournaments(
    tournament_service: tournament_serviceDP,
    offset: int = Query(default=0, ge=0, description="Смещение для пагинации"),
    limit: int = Query(default=50, le=500, description="Лимит записей на страницу"),
) -> list[Tournament]:
    return await tournament_service.get_tournaments(offset, limit)


@router.get("/{tournament_id}",
            response_model=TournamentResponse,
            description="Получение турниров по ID",
            summary="Get tournament by ID")
async def get_one_tournament(
    tournament_service: tournament_serviceDP, tournament_id: int
) -> TournamentBase:
    return await tournament_service.get_tournament(tournament_id)


@router.post("",
             dependencies=[Depends(get_current_admin)],
             response_model=TournamentResponse,
             description="Добавление записи о турнире в БД",
             summary="Add tournament to DB")
async def add_tournament(
    tournament_service: tournament_serviceDP, tournament_data: TournamentAdd
) -> TournamentBase:
    return await tournament_service.create_tournament(tournament_data)


@router.patch("/{tournament_id}",
              dependencies=[Depends(get_current_admin)],
              response_model=TournamentResponse,
              description="Обновление данных о турнире по ID",
              summary="Update tournament by ID")
async def update_tournament(
    tournament_service: tournament_serviceDP, tournament_id: int, tournament_data: TournamentUpdate
) -> TournamentBase:
    return await tournament_service.part_update_tournament(tournament_id, tournament_data)


@router.delete("/{tournament_id}",
               dependencies=[Depends(get_current_admin)],
               description="Удаление записи о турнире из БД по ID",
               summary="Delete tournament by ID")
async def del_tournament(tournament_service: tournament_serviceDP, tournament_id: int) -> bool:
    return await tournament_service.del_tournament(tournament_id)
