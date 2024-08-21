import os.path

from pydantic import BaseModel
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 15
    max_overflow: int = 10


class MainSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join("BOT", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__"
    )
    db: DatabaseConfig


settings = MainSettings()
print(settings.db.url)
