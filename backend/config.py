import functools

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


class DBConfig(BaseSettings):
    """Конфигурация БД"""

    driver: str
    host: str
    port: int | None = Field(default=None)
    username: str
    password: str
    name: str

    @functools.cached_property
    def db_url(self):
        return f"{self.driver}+asyncpg://{self.username}:{self.password}@{self.host}{f':{self.port}' if self.port else ''}/{self.name}"

    model_config = SettingsConfigDict(env_prefix="DB_", env_file=".env", extra="allow")


class JWTConfig(BaseSettings):
    """ Конфигурация JWT токена """
    secret_key: str
    algorithm: str

    model_config = SettingsConfigDict(env_prefix="JWT_", env_file=".env", extra="allow")

class YandexConfig(BaseSettings):
    """ Конфигурация Яндекс авторизации """
    client_id: str
    client_secret: str
    redirect_uri: str

    model_config = SettingsConfigDict(env_prefix="YANDEX_", env_file=".env", extra="allow")

# Инициализация конфигурации
db_config = DBConfig()
jwt_config = JWTConfig()
yandex_config = YandexConfig()

AUTHORIZATION_BASE_URL = "https://oauth.yandex.ru/authorize"
TOKEN_URL = "https://oauth.yandex.ru/token"

DATABASE_URL = db_config.db_url

engine = create_async_engine(DATABASE_URL)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)