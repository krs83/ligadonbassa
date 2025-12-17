from fastapi import Depends, HTTPException, status
from typing import Annotated
import jwt

from jwt import InvalidTokenError
from pydantic import ValidationError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.security import OAuth2PasswordBearer

from backend.src.config import settings
from backend.src.database import engine
from backend.src.models import User, Tournament
from backend.src.models.token import TokenData
from backend.src.repositories.general import Repository
from backend.src.services.athlete import AthleteService
from backend.src.services.athlete_tournament_link import AthleteTournamentLinkService
from backend.src.services.auth import AuthService
from backend.src.services.tournament import TournamentService
from backend.src.services.user import UserService

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login/access_token"
)

DPToken = Annotated[str, Depends(reusable_oauth2)]


async def get_session() -> AsyncSession:
    async with AsyncSession(engine) as session:
        yield session


DPSes = Annotated[AsyncSession, Depends(get_session)]


async def get_current_user(db: DPSes, token: DPToken) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenData(**payload)

    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    stmt = select(User).where(User.email == token_data.sub)
    res = await db.exec(stmt)
    user = res.first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_admin(current_user: CurrentUser) -> User:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges",
        )
    return current_user


def get_athlete_service(session: DPSes) -> AthleteService:
    repository = Repository(session)
    return AthleteService(repository)


athlete_serviceDP = Annotated[AthleteService, Depends(get_athlete_service)]


def get_user_service(session: DPSes) -> UserService:
    repository = Repository(session)
    return UserService(repository)


user_serviceDP = Annotated[UserService, Depends(get_user_service)]


def get_auth_service(session: DPSes) -> AuthService:
    repository = Repository(session)
    return AuthService(repository)


auth_serviceDP = Annotated[AuthService, Depends(get_auth_service)]


def get_tournament_service(session: DPSes) -> TournamentService:
    repository = Repository(session)
    return TournamentService(repository)


tournament_serviceDP = Annotated[TournamentService, Depends(get_tournament_service)]


def get_athlete_tournament_link_service(session: DPSes) -> AthleteTournamentLinkService:
    repository = Repository(session)
    return AthleteTournamentLinkService(repository)


athlete_tournament_link_serviceDP = Annotated[AthleteTournamentLinkService, Depends(get_athlete_tournament_link_service)]
