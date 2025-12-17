from datetime import date
from typing import TYPE_CHECKING

from sqlmodel import Field, SQLModel, String, Date, Relationship, Column

from backend.src.models import AthleteTournamentLink

if TYPE_CHECKING:
    from backend.src.models import Athlete


class TournamentBase(SQLModel):
    title: str = Field(String(50), index=True, nullable=False)
    smoothcomp_id: int = Field(nullable=False, unique=True)
    smoothcomp_date: date = Field(sa_column=Column(Date))


class Tournament(TournamentBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    athletes: list["Athlete"] = Relationship(
        back_populates="tournaments", link_model=AthleteTournamentLink
    )

class TournamentResponse(TournamentBase):
    id: int

class TournamentAdd(TournamentBase):
    pass

class TournamentUpdate(SQLModel):
    title: str | None = None
    smoothcomp_id:int | None = None
    smoothcomp_date: date | None = None
