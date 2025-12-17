from typing import TYPE_CHECKING

from sqlmodel import Field, SQLModel, String, Relationship

from backend.src.models import AthleteTournamentLink

if TYPE_CHECKING:
    from backend.src.models import Tournament

class AthleteBase(SQLModel):
    fullname: str = Field(String(50), index=True, nullable=False)
    category: str = Field(String(50), index=True, nullable=False)
    academy: str = Field(String(50), index=True, nullable=True)
    affiliation: str = Field(String(50), nullable=True )
    points: int = Field(index=True, default=0, ge=0)


class Athlete(AthleteBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    place: int | None = Field(default=None)

    tournaments: list["Tournament"] = Relationship(
        back_populates="athletes",  link_model=AthleteTournamentLink
    )


class AthleteResponse(AthleteBase):
    id: int
    place: int | None = None
    tournament_ids: list[int] | None = None


class AthleteAdd(AthleteBase):
    tournament_ids: list[int]


class AthleteUpdate(SQLModel):
    fullname: str | None = None
    category: str | None = None
    academy: str | None = None
    affiliation: str | None = None
    points: int | None = None

