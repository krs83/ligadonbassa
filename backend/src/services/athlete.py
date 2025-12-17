from typing import List

from sqlalchemy.exc import IntegrityError

from backend.src.exceptions.athlete import AthleteNotFoundException
from backend.src.exceptions.athlete_tournament_link import AthleteTournamentLinkIntegrityException
from backend.src.models.athlete import (
    AthleteAdd,
    AthleteResponse,
    Athlete,
    AthleteUpdate,
)
from backend.src.models.athlete_tournament import AthleteTournamentLinkAdd
from backend.src.services.base import BaseService


class AthleteService(BaseService):

    async def get_athletes(self, offset: int, limit: int) -> list[Athlete]:
        """Получение всех спортсменов из БД согласно выборке"""
        self.logger.info("Получен список всех спортсменов из БД согласно выборке")

        return await self.repository.athletes.get_athletes(offset=offset, limit=limit)

    async def get_athlete(self, athlete_id: int) -> Athlete:
        """Получение конкретного спортсмена по ID"""

        athlete =  await self.repository.athletes.get_athlete_by_id(athlete_id)
        if not athlete:
            self.logger.error(AthleteNotFoundException.ATHLETENOTFOUNDTEXT.format(athlete_id))
            raise AthleteNotFoundException(athlete_id)
        self.logger.info(f"Спортсмен с ID №{athlete_id} успешно получен")
        return athlete

    async def search_athlete_byname(self, athlete_data: str) -> Athlete:
        """Получение конкретного спортсмена по имени"""

        athlete =  await self.repository.athletes.get_athlete_by_name(athlete_data)
        if not athlete:
            self.logger.error(AthleteNotFoundException.ATHLETENOTFOUNDTEXT.format(athlete_data))
            raise AthleteNotFoundException(athlete_data)
        self.logger.info(f"Спортсмен с данными \"{athlete_data}\" успешно найден")
        return athlete

    async def create_athlete(self, athlete_data: AthleteAdd) -> AthleteResponse:
        """Добавление записи в БД о новом спортсмене"""

        athletes = await self.find_existing_athlete(athlete_data)
        athlete = athletes[0]

        await self.repository.athletes.create_athlete(athlete)

        try:
            for t_ids in athlete_data.tournament_ids:

                tournament_link_data = AthleteTournamentLinkAdd(athlete_id=athlete.id,
                                                                tournament_id=t_ids)

                await self.repository.athlete_tournament_links.create_athlete_tournament_link(tournament_link_data)
        except IntegrityError:
            self.logger.error(AthleteTournamentLinkIntegrityException.ATHLETETOURNAMENTLINKNOTFOUNDTEXT)
            raise AthleteTournamentLinkIntegrityException()

        self.logger.info("Добавлена новая связь атлет-турнир")
        await self.repository.athletes.calculating_place()

        await self.session.refresh(athlete)
        self.logger.info("Добавлен новый спортсмен")

        return  AthleteResponse(
            id=athlete.id,
            fullname=athlete.fullname,
            points=athlete.points,
            place=athlete.place,
            academy=athlete.academy,
            category=athlete.category,
            affiliation=athlete.affiliation,
            tournament_ids=athlete_data.tournament_ids
        )

    async def create_few_athletes(self, athlete_data: List[AthleteAdd]) -> List[AthleteResponse]:
        """Добавление списка новых спортсменов в БД"""

        athletes = await self.find_existing_athlete(athlete_data)

        await self.repository.athletes.create_few_athletes(athletes)

        try:
            for athlete_add, athlete_db in zip(athlete_data, athletes):
                for t_id in athlete_add.tournament_ids:

                    tournament_link_data = AthleteTournamentLinkAdd(athlete_id=athlete_db.id,
                                                                tournament_id=t_id)

                    await self.repository.athlete_tournament_links.create_athlete_tournament_link(tournament_link_data)
                    await self.repository.athletes.calculating_place()

                    for athlete in athletes:
                        await self.session.refresh(athlete)
                    self.logger.info("Массовое добавление спортсменов")
        except IntegrityError:
            self.logger.error(AthleteTournamentLinkIntegrityException.ATHLETETOURNAMENTLINKNOTFOUNDTEXT)
            raise AthleteTournamentLinkIntegrityException()

        self.logger.info("Добавлены новые связи атлет-турнир")


        return [
            AthleteResponse(
                id=athlete_db.id,
                fullname=athlete_add.fullname,
                category=athlete_add.category,
                academy=athlete_add.academy,
                affiliation=athlete_add.affiliation,
                points=athlete_add.points,
                place=athlete_db.place if athlete_db.place is not None else "-",
                tournament_ids=athlete_add.tournament_ids
            )
            for athlete_add, athlete_db in zip(athlete_data, athletes)
        ]

    async def part_update_athlete(self, athlete_id: int, athlete_data: AthleteUpdate) -> AthleteResponse:
        """Частичное или полное обновление данных о спортсмене по его ID"""

        athlete = athlete_data.model_dump(exclude_unset=True)

        db_athlete = await self.repository.athletes.update_athlete(
            athlete_id=athlete_id, athlete_data=athlete
        )
        if not db_athlete:
            self.logger.error(AthleteNotFoundException.ATHLETENOTFOUNDTEXT.format(athlete_id))
            raise AthleteNotFoundException(athlete_id)
        await self.repository.athletes.calculating_place()
        await self.session.refresh(db_athlete)
        self.logger.info(f"Спортсмен с ID №{athlete_id} успешно обновлён")

        return AthleteResponse.model_validate(db_athlete)

    async def del_athlete(self, athlete_id: int) -> bool:
        """Удаление записи о спортсмене из БД по его ID"""

        athlete =  await self.repository.athletes.delete_athlete(athlete_id)
        await self.repository.athletes.calculating_place()
        if not athlete:
            self.logger.error(AthleteNotFoundException.ATHLETENOTFOUNDTEXT.format(athlete_id))
            raise AthleteNotFoundException(athlete_id)
        self.logger.info(f"Спортсмен с ID №{athlete_id} успешно удалён")

        return athlete


    async def find_existing_athlete(self, athletes_data: AthleteAdd | List[AthleteAdd]) -> List[Athlete]:
        """Если будет совпадение по имени, ДР и региону, новый спортсмен не добавляется\n
       Только суммируются баллы\n
        В противном случае - добавляется новый спортсмен
        """

        if not isinstance(athletes_data, list):
            athletes_data = [athletes_data]

        list_athletes = []
        for athlete_data in athletes_data:

            athlete = await self.repository.athletes.get_athlete_by_conditions(athlete_data)

            if athlete:
                athlete.points += athlete_data.points
                list_athletes.append(athlete)
                self.logger.info(f"Баллы спортсмена обновлены - {athlete.points} ")

            else:
                new_athlete = Athlete.model_validate(athlete_data)
                list_athletes.append(new_athlete)

            self.logger.info("Добавлен новый спортсмен")

        return list_athletes






