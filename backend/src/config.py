from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    SITENAME: str

    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_WEEKS: int
    API_V1_STR: str = "/api/v1"

    ADMIN_LOGIN: str | None = None
    ADMIN_PASSWORD: str | None = None

    POSTGRES_PASSWORD: str | None = None
    POSTGRES_USER: str | None = None
    POSTGRES_DB: str | None = None

    HEADER_IMAGE: str = "/static/images/ligadonbassa.jpg"
    LIGADONBASSA_IMAGE_1: str = "/static/images/ligadonbassa_25_10_25.jpg"
    LIGADONBASSA_IMAGE_2: str = "/static/images/ligadonbassa_20_12_25.png"

    #Для локально разработки .env.local, для докера - .env.docker
    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env.local")


settings = Settings()
