from datetime import timezone, timedelta
from pydantic import BaseSettings, Field
from pydantic.types import SecretStr


class Settings(BaseSettings):
    debug: bool = False
    tz: timezone = timezone(timedelta(hours=7))
    pg_host: str = Field("localhost", env="POSTGRES_HOST")
    pg_port: int = 5432
    pg_user: str = Field("admin", env="POSTGRES_USER")
    pg_password: SecretStr = Field("mypassword", env="POSTGRES_PASSWORD")
    pg_dbname: str = Field("pokemon", env="POSTGRES_DB")


settings = Settings()
