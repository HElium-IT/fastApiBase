from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    API_V1_STR: str
    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_PASSWORD: str

    USERS_OPEN_REGISTRATION: bool

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int
    JWT_PUBLIC_KEY: str
    JWT_PRIVATE_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    JWT_ALGORITHM: str

    CLIENT_ORIGIN: str

    class Config:
        env_file = '/app/.env'


settings = Settings()