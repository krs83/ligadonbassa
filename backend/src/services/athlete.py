from typing import List

from sqlalchemy.exc import IntegrityError

from backend.src.exceptions.athlete import AthleteNotFoundException
from backend.src.exceptions.tournament import TournamentNotFoundException
from backend.src.exceptions.athlete_tournament_link import AthleteTournamentLinkIntegrityException
from backend.src.models.athlete import (
    AthleteCreate,
    AthleteResponse,
    Athlete,
    AthleteUpdate,
)
from backend.src.models.athlete_tournament import AthleteTournamentLinkAdd
from backend.src.models.tournament import TournamentPatch
from backend.src.services.base import BaseService


class AthleteService(BaseService):

    async def get_athletes(self, offset: int, limit: int) -> list[Athlete]:
        """Получение всех спортсменов из БД согласно выборке"""
        self.logger.info("Получен список всех спортсменов из БД согласно выборке")

        return await self.repository.athletes.get_athletes(offset=offset, limit=limit)

    async def admin_get_athletes(self, offset: int, limit: int) -> list[Athlete]:
        """Получение всех спортсменов из БД согласно выборке, включая неактивных"""
        self.logger.info("Получен список всех спортсменов из БД согласно выборке, включая неактивных")

        return await self.repository.athletes.get_athletes(offset=offset, limit=limit, is_admin=True)

    async def get_athlete(self, athlete_id: int) -> Athlete:
        """Получение конкретного спортсмена по ID"""

        athlete =  await self.repository.athletes.get_athlete_by_id(athlete_id)
        if not athlete:
            self.logger.error(AthleteNotFoundException.ATHLETENOTFOUNDTEXT.format(athlete_id))
            raise AthleteNotFoundException(athlete_id)
        self.logger.info(f"Спортсмен с ID №{athlete_id} успешно получен")
        return athlete

    async def admin_get_athlete(self, athlete_id: int) -> Athlete:
        """Получение конкретного спортсмена по ID, включая неактивного"""

        athlete =  await self.repository.athletes.admin_get_athlete_by_id(athlete_id)
        if not athlete:
            self.logger.error(AthleteNotFoundException.ATHLETENOTFOUNDTEXT.format(athlete_id))
            raise AthleteNotFoundException(athlete_id)
        self.logger.info(f"Спортсмен с ID №{athlete_id} (НЕАКТИВНЫЙ) успешно получен")
        return athlete

    async def search_athlete_by_name(self, athlete_data: str) -> Athlete | list:
        """Получение конкретного спортсмена по имени"""

        athlete =  await self.repository.athletes.get_athlete_by_name(athlete_data)
        if not athlete:
            return []
        self.logger.info(f"Спортсмен с данными \"{athlete_data}\" успешно найден")
        return athlete

    async def create_athlete(self, athlete_data: AthleteCreate) -> AthleteResponse:
        """Добавление записи в БД о новом спортсмене"""

        #проверка правильный ли id турнира
        for t_id in athlete_data.tournament_ids:
            tournament = await self.repository.tournaments.get_tournament_by_id(t_id)
            if not tournament:
                self.logger.error(TournamentNotFoundException.TOURNAMENTNOTFOUNDTEXT.format(t_id))
                raise TournamentNotFoundException(t_id)


        athletes = await self.find_existing_athlete(athlete_data)
        athlete = athletes[0]

        athlete = await self.repository.athletes.create_athlete(athlete)

        try:
            for t_id in athlete_data.tournament_ids:

                tournament_link_data = AthleteTournamentLinkAdd(athlete_id=athlete.id,
                                                                tournament_id=t_id)

                await self.repository.athlete_tournament_links.create_athlete_tournament_link(tournament_link_data)
                await self.repository.athletes.calculating_place()
                await self.session.refresh(athlete)
        except IntegrityError:
            self.logger.error(AthleteTournamentLinkIntegrityException.ATHLETETOURNAMENTLINKNOTFOUNDTEXT)
            raise AthleteTournamentLinkIntegrityException()

        self.logger.info("Добавлена новая связь атлет-турнир")
        self.logger.info("Добавлен новый спортсмен")

        return AthleteResponse.model_validate(athlete)

    async def create_few_athletes(self, athlete_data: List[AthleteCreate]) -> List[AthleteResponse]:
        """Добавление списка новых спортсменов в БД"""
        #проверка правильный ли id турнира
        for data in athlete_data:
            for t_id in data.tournament_ids:
                tournament = await self.repository.tournaments.get_tournament_by_id(t_id)
                if not tournament:
                    self.logger.error(TournamentNotFoundException.TOURNAMENTNOTFOUNDTEXT.format(t_id))
                    raise TournamentNotFoundException(t_id)

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
                fullname=athlete_db.fullname,
                category=athlete_db.category,
                academy=athlete_db.academy,
                affiliation=athlete_db.affiliation,
                points=athlete_db.points,
                place=athlete_db.place if athlete_db.place is not None else 0,
                is_active=athlete_db.is_active,
                tournaments=athlete_db.tournaments
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

        try:
            # обновляем список турниров, в котором участвовал спортсмен
            if athlete_data.tournament_ids:
                t_ids = [TournamentPatch(id=t_id) for t_id in athlete_data.tournament_ids]

                await self.repository.tournaments.refresh_athletes_tournaments(athlete_id=athlete_id,
                                                                               tournaments=t_ids)
        except IntegrityError:
            self.logger.error(TournamentNotFoundException.TOURNAMENTNOTFOUNDTEXT.format(athlete_data.tournament_ids))
            raise TournamentNotFoundException(athlete_data.tournament_ids)

        #берем данные из БД для показа в AthleteResponse
        updated_athlete = await self.repository.athletes.get_athlete_by_id(athlete_id)

        self.logger.info(f"Спортсмен с ID №{athlete_id} успешно обновлён")

        return AthleteResponse.model_validate(updated_athlete)

    async def soft_del_athlete(self, athlete_id: int) -> dict:
        """Мягкое удаление записи о спортсмене из БД по его ID"""

        athlete =  await self.repository.athletes.soft_delete_athlete(athlete_id)
        await self.repository.athletes.calculating_place()
        if not athlete:
            self.logger.error(AthleteNotFoundException.ATHLETENOTFOUNDTEXT.format(athlete_id))
            raise AthleteNotFoundException(athlete_id)
        self.logger.info(f"Спортсмен с ID №{athlete_id} помечен как неактивный")

        return {"message": f"Спортсмен с ID №{athlete_id} помечен как неактивный"}

    async def restoring_athlete(self, athlete_id: int) -> dict:
        """Восстановление записи о спортсмене по его ID"""

        athlete =  await self.repository.athletes.restore_athlete(athlete_id)
        await self.repository.athletes.calculating_place()
        if not athlete:
            self.logger.error(AthleteNotFoundException.ATHLETENOTFOUNDTEXT.format(athlete_id))
            raise AthleteNotFoundException(athlete_id)
        self.logger.info(f"Спортсмен с ID №{athlete_id} восстановлен и помечен как активный")

        return {"message": f"Спортсмен с ID №{athlete_id} восстановлен и помечен как активный"}


    async def find_existing_athlete(self, athletes_data: AthleteCreate | List[AthleteCreate]) -> List[Athlete]:
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

        return list_athletes






