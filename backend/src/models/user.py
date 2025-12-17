from sqlmodel import Field, SQLModel
from pydantic import EmailStr


class UserBase(SQLModel):
    email: EmailStr = Field(nullable=False, index=True, unique=True, max_length=255)
    is_admin: bool = Field(default=False)


class UserCreate(UserBase):
    password: str = Field(min_length=6, max_length=40)


class UserUpdate(UserBase):
    email: EmailStr | None = None
    password: str | None = None


class UserUpdateMe(SQLModel):
    email: EmailStr | None = None


class UserUpdatePassword(SQLModel):
    current_password: str = Field(min_length=6, max_length=40)
    new_password: str = Field(min_length=6, max_length=40)


class UserLogin(SQLModel):
    email: EmailStr
    password: str


class UserResponse(UserBase):
    id: int


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str = Field(max_length=200)
