import functools

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


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
        return f"{self.driver}://{self.username}:{self.password}@{self.host}{f':{self.port}' if self.port else ''}/{self.name}"

    model_config = SettingsConfigDict(env_prefix="DB_", env_file=".env", extra="allow")


class JWTConfig(BaseSettings):
    secret_key: str
    algorithm: str

    model_config = SettingsConfigDict(env_prefix="JWT_", env_file=".env")

# Инициализация конфигурации
db_config = DBConfig()
jwt_config = JWTConfig()