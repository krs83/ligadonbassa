from typing import Any, List

from sqlmodel import asc, desc

from backend.src.models.athlete import Athlete, AthleteCreate
from backend.src.repositories.base import BaseRepository


class AthleteRepository(BaseRepository):

    async def get_athletes(self,
                           offset: int | None = None,
                           limit: int | None = None,
                           order_by=None,
                           is_admin=False) -> list[Athlete]:

        if order_by is None:
            order_by = asc(Athlete.place)

        return await self._get_many(
            model=Athlete,
            conditions=None if is_admin else [Athlete.is_active == True],
            link_model=Athlete.tournaments,
            offset=offset,
            limit=limit,
            order_by=order_by,
            link=True,
        )

    async def get_athlete_by_id(self, athlete_id: int) -> Athlete:
        return await self._get_pk(model=Athlete, pk=athlete_id, link_model=Athlete.tournaments, link=True)

    async def admin_get_athlete_by_id(self, athlete_id: int) -> Athlete:
        return await self._get_pk(model=Athlete,
                                  pk=athlete_id,
                                  link_model=Athlete.tournaments,
                                  link=True,
                                  is_admin=True)

    async def get_athlete_by_conditions(self, athlete_data: AthleteCreate) -> Athlete:
        return await self._get_one(
            Athlete,
            Athlete.fullname == athlete_data.fullname,
            Athlete.category == athlete_data.category,
            Athlete.affiliation == athlete_data.affiliation,
        )

    async def get_athlete_by_name(self, athlete_data: str) -> Athlete:
        return await self._get_many_by_conditions(
            Athlete,
            Athlete.fullname.ilike(f"%{athlete_data}%"),
            )

    async def create_athlete(self, db_athlete: Athlete) -> Athlete:
        self.session.add(db_athlete)
        await self.session.commit()
        await self.session.refresh(db_athlete)
        return db_athlete

    async def create_few_athletes(self, db_athlete: List[Athlete]) -> List[Athlete]:
        self.session.add_all(db_athlete)
        await self.session.commit()
        for athlete in db_athlete:
            await self.session.refresh(athlete)
        return db_athlete

    async def update_athlete(
            self, athlete_id: int, athlete_data: dict[str, Any]
    ) -> Athlete | None:
        db_athlete = await self._update(Athlete, athlete_data, athlete_id)
        if db_athlete is not None:
            await self.session.commit()
            await self.session.refresh(db_athlete)
            return db_athlete
        return None

    async def soft_delete_athlete(self, athlete_id: int) -> Athlete | None:
            result = await self._get_pk(model=Athlete, pk=athlete_id, link_model=Athlete.tournaments, link=True)
            if result:
                result.is_active = False
                await self.session.commit()
                return result
            else:
                return None

    async def restore_athlete(self, athlete_id: int) -> Athlete | None:
        result = await self._get_pk(model=Athlete, pk=athlete_id, link_model=Athlete.tournaments, link=True)
        if result:
            result.is_active = True
            await self.session.commit()
            return result
        else:
            return None

    async def calculating_place(self) -> None:
        athletes = await self.get_athletes(order_by=desc(Athlete.points))

        for i, athlete in enumerate(athletes, start=1):
            athlete.place = i

        await self.session.commit()
