from typing import Any

from sqlmodel import asc

from backend.src.models import Athlete, AthleteTournamentLink
from backend.src.models.athlete_tournament import AthleteTournamentLinkAdd
from backend.src.models.tournament import Tournament, TournamentPatch
from backend.src.repositories.athlete_tournament_link import AthleteTournamentLinkRepository
from backend.src.repositories.base import BaseRepository


class TournamentRepository(BaseRepository):

    async def get_tournaments(self,
                           offset: int,
                           limit: int,
                           order_by=asc(Tournament.smoothcomp_date)) ->list[Tournament]:

        result = await self._get_many(
            model=Tournament, offset=offset, limit=limit, order_by=order_by
        )
        return result

    async def get_tournament_by_id(self, tournament_id: int) -> Tournament:
        return await self._get_pk(model=Tournament, pk=tournament_id)


    async def create_tournament(self, db_tournament: Tournament) -> Tournament:
        self.session.add(db_tournament)
        await self.session.commit()
        await self.session.refresh(db_tournament)
        return db_tournament


    async def update_tournament(
        self, tournament_id: int, tournament_data: dict[str, Any]
    ) -> Tournament | None:
        db_tournament = await self._update(Tournament, tournament_data, tournament_id)
        if db_tournament is not None:
            await self.session.commit()
            await self.session.refresh(db_tournament)
            return db_tournament
        return None

    async def delete_tournament(self, tournament_id: int) -> bool:
        result = await self._delete(Tournament, Tournament.id == tournament_id)
        return result

    async def refresh_athletes_tournaments(self, athlete_id: int, tournaments: list[TournamentPatch]) -> None:

        new_tournaments_ids = {t.id for t in tournaments}
        current_tournaments_ids = await self._get_pk(model=Athlete,
                                                     pk=athlete_id,
                                                     link_model=Athlete.tournaments,
                                                     link=True)
        current_tournaments_ids = {i.id for i in current_tournaments_ids.tournaments}

        to_remove = current_tournaments_ids - new_tournaments_ids
        to_add = new_tournaments_ids - current_tournaments_ids

        if to_remove:
            await self._delete(AthleteTournamentLink,
                               AthleteTournamentLink.athlete_id == athlete_id,
                               AthleteTournamentLink.tournament_id.in_(to_remove),
                             )
        if to_add:
            for t_id in to_add:
                tournament_link_data = AthleteTournamentLinkAdd(athlete_id=athlete_id,
                                                                tournament_id=t_id)
                repo = AthleteTournamentLinkRepository(session=self.session)
                await repo.create_athlete_tournament_link(tournament_link_data)
