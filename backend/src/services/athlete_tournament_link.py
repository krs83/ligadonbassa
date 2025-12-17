from sqlalchemy.exc import IntegrityError

from backend.src.exceptions.athlete_tournament_link import AthleteTournamentLinkIntegrityException
from backend.src.models.athlete_tournament import (AthleteTournamentLinkAdd,
                                                   AthleteTournamentLinkResponse,
                                                   AthleteTournamentLink)
from backend.src.services.base import BaseService


class AthleteTournamentLinkService(BaseService):

    # async def get_tournaments(self, offset: int, limit: int) -> list[Tournament]:
    #     """Получение всех турниров из БД согласно выборке"""
    #     self.logger.info("Получен список всех турниров из БД согласно выборке")
    #
    #     return await self.repository.tournaments.get_tournaments(offset=offset, limit=limit)
    #
    # async def get_tournament(self, tournament_id: int) -> Tournament:
    #     """Получение конкретного турнира по ID"""
    #
    #     tournament =  await self.repository.tournaments.get_tournament_by_id(tournament_id)
    #     if not tournament:
    #         self.logger.error(TournamentNotFoundException.TOURNAMENTNOTFOUNDTEXT.format(tournament_id))
    #         raise TournamentNotFoundException(tournament_id)
    #     self.logger.info(f"Турнир с ID №{tournament_id} успешно получен")
    #     return tournament

    async def create_athlete_tournament_link(self,
                                             athlete_tournament_link_data:
                                             AthleteTournamentLinkAdd) -> AthleteTournamentLinkResponse:
        """Добавление связи в БД о новом атлете-турнире"""

        try:
            link = AthleteTournamentLink.model_validate(athlete_tournament_link_data)

            await self.repository.athlete_tournament_links.create_athlete_tournament_link(athlete_tournament_link_data)
        except IntegrityError:
            self.logger.error(AthleteTournamentLinkIntegrityException.ATHLETETOURNAMENTLINKNOTFOUNDTEXT)
            raise AthleteTournamentLinkIntegrityException()

        self.logger.info("Добавлена новая связь атлет-турнир")

        return AthleteTournamentLinkResponse.model_validate(link)


    # async def part_update_tournament(self, tournament_id: int, tournament_data: TournamentUpdate) -> TournamentResponse:
    #     """Частичное или полное обновление данных о турнире по ID"""
    #
    #     tournament = tournament_data.model_dump(exclude_unset=True)
    #
    #     db_tournament = await self.repository.tournaments.update_tournament(
    #         tournament_id=tournament_id, tournament_data=tournament
    #     )
    #     if not db_tournament:
    #         self.logger.error(TournamentNotFoundException.TOURNAMENTNOTFOUNDTEXT.format(tournament_id))
    #         raise TournamentNotFoundException(tournament_id)
    #     self.logger.info(f"Турнир с ID №{tournament_id} успешно обновлён")
    #
    #     return TournamentResponse.model_validate(db_tournament)
    #
    async def del_athlete_tournament_link(self, athlete_id: int, tournament_id: int) -> bool:
        """Удаление связи о спорсмене-турнире из БД по ID"""

        link =  await self.repository.athlete_tournament_links.delete_athlete_tournament_link(athlete_id,
                                                                                                    tournament_id)
        if not link:
            self.logger.error(AthleteTournamentLinkIntegrityException.ATHLETETOURNAMENTLINKNOTFOUNDTEXT)
            raise AthleteTournamentLinkIntegrityException()
        self.logger.info(f"Связь успешно удалёна")

        return link





