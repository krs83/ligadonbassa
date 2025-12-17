from sqlmodel import SQLModel


class Token(SQLModel):
    access_token: str
    token_type: str = "Bearer"


class TokenData(SQLModel):
    sub: str | None = None
