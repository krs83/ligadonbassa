from sqlalchemy.exc import IntegrityError

from backend.src.exceptions.tournament import TournamentNotFoundException, TournamentIntegrityException
from backend.src.models.tournament import (
    TournamentAdd,
    TournamentResponse,
    Tournament,
    TournamentUpdate,
)
from backend.src.services.base import BaseService


class TournamentService(BaseService):

    async def get_tournaments(self, offset: int, limit: int) -> list[Tournament]:
        """Получение всех турниров из БД согласно выборке"""
        self.logger.info("Получен список всех турниров из БД согласно выборке")

        return await self.repository.tournaments.get_tournaments(offset=offset, limit=limit)

    async def get_tournament(self, tournament_id: int) -> Tournament:
        """Получение конкретного турнира по ID"""

        tournament =  await self.repository.tournaments.get_tournament_by_id(tournament_id)
        if not tournament:
            self.logger.error(TournamentNotFoundException.TOURNAMENTNOTFOUNDTEXT.format(tournament_id))
            raise TournamentNotFoundException(tournament_id)
        self.logger.info(f"Турнир с ID №{tournament_id} успешно получен")
        return tournament

    async def create_tournament(self, tournament_data: TournamentAdd) -> TournamentResponse:
        """Добавление записи в БД о новом турнире"""

        try:
            tournament = Tournament.model_validate(tournament_data)

            await self.repository.tournaments.create_tournament(tournament)
        except IntegrityError:
            self.logger.error(TournamentIntegrityException.TOURNAMENTINTEGRITYTEXT.format(tournament_data.smoothcomp_id))
            raise TournamentIntegrityException(tournament_data.smoothcomp_id)

        self.logger.info("Добавлен новый турнир")

        return TournamentResponse.model_validate(tournament)


    async def part_update_tournament(self, tournament_id: int, tournament_data: TournamentUpdate) -> TournamentResponse:
        """Частичное или полное обновление данных о турнире по ID"""

        tournament = tournament_data.model_dump(exclude_unset=True)

        db_tournament = await self.repository.tournaments.update_tournament(
            tournament_id=tournament_id, tournament_data=tournament
        )
        if not db_tournament:
            self.logger.error(TournamentNotFoundException.TOURNAMENTNOTFOUNDTEXT.format(tournament_id))
            raise TournamentNotFoundException(tournament_id)
        self.logger.info(f"Турнир с ID №{tournament_id} успешно обновлён")

        return TournamentResponse.model_validate(db_tournament)

    async def del_tournament(self, tournament_id: int) -> bool:
        """Удаление записи о турнире из БД по ID"""

        tournament =  await self.repository.tournaments.delete_tournament(tournament_id)
        if not tournament:
            self.logger.error(TournamentNotFoundException.TOURNAMENTNOTFOUNDTEXT.format(tournament_id))
            raise TournamentNotFoundException(tournament_id)
        self.logger.info(f"Турнир с ID №{tournament_id} успешно удалён")

        return tournament






