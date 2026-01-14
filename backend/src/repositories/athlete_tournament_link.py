from sqlmodel import asc

from backend.src.models import AthleteTournamentLink
from backend.src.models.athlete_tournament import AthleteTournamentLinkAdd
from backend.src.repositories.base import BaseRepository


class AthleteTournamentLinkRepository(BaseRepository):

    async def get_athlete_tournament_links(self,
                              offset: int,
                              limit: int,
                              order_by=asc(AthleteTournamentLink.athlete_id)) ->list[AthleteTournamentLink]:

        result = await self._get_many(
            model=AthleteTournamentLink, offset=offset, limit=limit, order_by=order_by
        )
        return result

    async def create_athlete_tournament_link(self,
                                             athlete_tournament_link_data: AthleteTournamentLinkAdd) -> AthleteTournamentLink:
        link = AthleteTournamentLink.model_validate(athlete_tournament_link_data)
        self.session.add(link)
        await self.session.commit()
        await self.session.refresh(link)
        return link


    async def delete_athlete_tournament_link(self, athlete_id: int, tournament_id: int) -> bool:
        result = await self._delete(AthleteTournamentLink,
                                    AthleteTournamentLink.athlete_id == athlete_id,
                                    AthleteTournamentLink.tournament_id == tournament_id,)
        return result

