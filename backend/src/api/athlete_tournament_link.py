from fastapi import APIRouter, Query, Depends

from backend.src.dependencies import  get_current_admin, athlete_tournament_link_serviceDP

from backend.src.models.athlete_tournament import AthleteTournamentLinkResponse, AthleteTournamentLinkBase, \
    AthleteTournamentLinkAdd

router = APIRouter(prefix="/athlete_tournament_link", tags=["Спортсмен-турнир-связь"])

@router.get("",
            response_model=list[AthleteTournamentLinkResponse],
            description="Получение списка всех связей спортсменов-турниров",
            summary="Get all athletes-tournaments list links")
async def get_all_athlete_tournament_links(
        athlete_tournament_link_service: athlete_tournament_link_serviceDP,
        offset: int = Query(default=0, ge=0, description="Смещение для пагинации"),
        limit: int = Query(default=50, le=500, description="Лимит записей на страницу"),
) -> list[AthleteTournamentLinkBase]:
    return await athlete_tournament_link_service.get_athlete_tournament_links(offset, limit)

@router.post("",
             dependencies=[Depends(get_current_admin)],
             response_model=AthleteTournamentLinkResponse,
             description="Добавление связи спортсмен-турнир в БД",
             summary="Add athlete tournament link to DB")
async def add_athlete_tournament_link(
        athlete_tournament_link_service: athlete_tournament_link_serviceDP,
        athlete_tournament_link_data: AthleteTournamentLinkAdd
) -> AthleteTournamentLinkBase:
    return await athlete_tournament_link_service.create_athlete_tournament_link(athlete_tournament_link_data)


@router.delete("/{athlete_id}/{tournament_id}",
               dependencies=[Depends(get_current_admin)],
               description="Удаление связи о спортсмене-турнире из БД по ID",
               summary="Delete athlete_tournament_link by ID")
async def del_athlete_tournament_link(athlete_tournament_link_service: athlete_tournament_link_serviceDP,
                      athlete_id: int,
                      tournament_id: int) -> bool:
    return await athlete_tournament_link_service.del_athlete_tournament_link(athlete_id, tournament_id)
