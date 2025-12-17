from sqlmodel.ext.asyncio.session import AsyncSession

from backend.src.repositories.athlete import AthleteRepository
from backend.src.repositories.athlete_tournament_link import AthleteTournamentLinkRepository
from backend.src.repositories.base import BaseRepository
from backend.src.repositories.tournament import TournamentRepository
from backend.src.repositories.user import UserRepository


class Repository(BaseRepository):
    athletes: AthleteRepository
    users: UserRepository
    tournaments: TournamentRepository
    athlete_tournament_links: AthleteTournamentLinkRepository

    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.athletes = AthleteRepository(session=session)
        self.users = UserRepository(session=session)
        self.tournaments = TournamentRepository(session=session)
        self.athlete_tournament_links = AthleteTournamentLinkRepository(session=session)
