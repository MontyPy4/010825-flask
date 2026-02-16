from pathlib import Path
from typing import Any

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    # project info
    app_name: str
    debug: bool = False

    # DB settings
    mysql_host: SecretStr # скрывается реальное значение
    mysql_port: int
    mysql_user: str
    mysql_password: SecretStr
    my_pool_size: int # максимальное количество подключений
    mysql_pool_timeout: int # максимальное время ожидания подключения

    # API settings
    api_prefix: str
    api_version: str

    model_config = SettingsConfigDict(  # будет искать все верхние настройки в файле .env
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )

@property
def get_flask_config(self) -> dict[str, Any]:
    return {
        "DEBUG": self.debug,
        "SQLALCHEMY_DATABASE_URI": self.database_url,
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "SQLALCHEMY_POOL_SIZE": self.mysql_pool_size,
        "SQLALCHEMY_POOL_TIMEOUT": self.mysql_pool_timeout,
    }


settings = Settings()

print(settings)
print(settings.get_flask_config)