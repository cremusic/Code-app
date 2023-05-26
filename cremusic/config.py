from datetime import timezone, timedelta
from pydantic import BaseSettings
from pydantic.types import SecretStr


class Settings(BaseSettings):
    debug: bool = False
    tz: timezone = timezone(timedelta(hours=7))
    pg_host: str = "localhost"
    pg_port: int = 5432
    pg_user: str = "admin"
    pg_password: SecretStr = SecretStr("mypassword")
    pg_dbname: str = "pokemon"


settings = Settings()
