from typing import Any

from backend.src.models.tournament import Tournament
from backend.src.repositories.base import BaseRepository


class TournamentRepository(BaseRepository):

    async def get_tournaments(self,
                           offset: int,
                           limit: int,
                           order_by=Tournament.smoothcomp_date.asc()) ->list[Tournament]:

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
        await self.session.commit()
        return result

