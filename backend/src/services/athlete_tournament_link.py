from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError

from backend.src.exceptions.athlete_tournament_link import AthleteTournamentLinkIntegrityException
from backend.src.models.athlete_tournament import (AthleteTournamentLinkAdd,
                                                   AthleteTournamentLinkResponse,
                                                   AthleteTournamentLink)
from backend.src.services.base import BaseService


class AthleteTournamentLinkService(BaseService):

    async def get_athlete_tournament_links(self, offset: int, limit: int) -> list[AthleteTournamentLink]:
        """Получение всех связей спортсменов-турниров из БД согласно выборке"""
        self.logger.info("Получен список всех связей спортсменов-турниров из БД согласно выборке")

        return await self.repository.athlete_tournament_links.get_athlete_tournament_links(offset, limit)

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

    async def del_athlete_tournament_link(self, athlete_id: int, tournament_id: int) -> bool:
        """Удаление связи о спорсмене-турнире из БД по ID"""

        link =  await self.repository.athlete_tournament_links.delete_athlete_tournament_link(athlete_id,
                                                                                                    tournament_id)
        if not link:
            self.logger.error(AthleteTournamentLinkIntegrityException.ATHLETETOURNAMENTLINKNOTFOUNDTEXT)
            raise AthleteTournamentLinkIntegrityException()
        self.logger.info(f"Связь успешно удалёна")

        return link





