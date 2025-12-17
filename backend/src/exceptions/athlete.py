from backend.src.exceptions.base import NotFoundException



class AthleteNotFoundException(NotFoundException):
    ATHLETENOTFOUNDTEXT = "Спортсмен с ID №{} не найден"

    def __init__(self, athlete_id: int):
        super().__init__(detail=self.ATHLETENOTFOUNDTEXT.format(athlete_id))