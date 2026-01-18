from typing import TYPE_CHECKING, Any
from pydantic import field_validator

from sqlmodel import Field, SQLModel, String, Relationship

from backend.src.models import AthleteTournamentLink
from backend.src.models.tournament import TournamentResponse

if TYPE_CHECKING:
    from backend.src.models import Tournament

class AthleteBase(SQLModel):
    fullname: str = Field(String(50), index=True, nullable=False)
    category: str = Field(String(50), index=True, nullable=False)
    academy: str = Field(String(50), index=True, nullable=True)
    activity: float = Field(default=1.0, nullable=False, ge=0.5, le=1.5)
    points: int = Field(index=True, default=0, ge=0)

    @field_validator("activity", mode="before")
    def normalize_activity(cls, v: Any):
        if v is None:
            return None
        return max(0.5, min(v, 1.5))

    @field_validator("points", mode="before")
    def normalize_points(cls, v: Any):
        if v is None:
            return None
        return max(0, v)


class Athlete(AthleteBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    is_active: bool = Field(default=True)
    place: int | None = Field(default=None)
    calc_points: float = Field(default=0.0, index=True)

    tournaments: list["Tournament"] = Relationship(
        back_populates="athletes",
        link_model=AthleteTournamentLink,
        sa_relationship_kwargs={"lazy": "selectin"}
    )

class AthleteResponse(AthleteBase):
    id: int
    place: int | None = None
    tournaments: list[TournamentResponse] = []
    calc_points: float = 0.0
    is_active: bool


class AthleteCreate(AthleteBase):
    tournament_ids: list[int] = []


class AthleteUpdate(AthleteBase):
    fullname: str | None = None
    category: str | None = None
    academy: str | None = None
    activity: float | None = None
    points: int | None = None
    tournament_ids: list[int] | None = None
