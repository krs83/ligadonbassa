from sqlmodel import Field, SQLModel


class AthleteTournamentLinkBase(SQLModel):
    athlete_id: int
    tournament_id: int


class AthleteTournamentLink(SQLModel, table=True):
    athlete_id: int | None = Field(
        default=None, foreign_key="athlete.id", primary_key=True
    )
    tournament_id: int | None = Field(
        default=None, foreign_key="tournament.id", primary_key=True
    )


class AthleteTournamentLinkAdd(AthleteTournamentLinkBase):
    pass

class AthleteTournamentLinkResponse(AthleteTournamentLinkBase):
    pass


