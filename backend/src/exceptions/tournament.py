from backend.src.exceptions.base import NotFoundException, ConflictException


class TournamentNotFoundException(NotFoundException):
    TOURNAMENTNOTFOUNDTEXT = "Турнир с ID №{} не найден"

    def __init__(self, tournament_id: int):
        super().__init__(detail=self.TOURNAMENTNOTFOUNDTEXT.format(tournament_id))


class TournamentIntegrityException(ConflictException):
    TOURNAMENTINTEGRITYTEXT = "Турнир с ID №{} уже существует"

    def __init__(self, tournament_id: int):
        super().__init__(detail=self.TOURNAMENTINTEGRITYTEXT.format(tournament_id))