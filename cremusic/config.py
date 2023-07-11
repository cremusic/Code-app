from datetime import timezone, timedelta
from pydantic import BaseSettings, Field
from pydantic.types import SecretStr


class Settings(BaseSettings):
    tz: timezone = timezone(timedelta(hours=7))
    debug: bool = Field(False, env="DEBUG")
    pg_host: str = Field("localhost", env="POSTGRES_HOST")
    pg_port: int = 5432
    pg_user: str = Field("admin", env="POSTGRES_USER")
    pg_password: SecretStr = Field("mypassword", env="POSTGRES_PASSWORD")
    pg_dbname: str = Field("pokemon", env="POSTGRES_DB")

    admin_secret_key: SecretStr = Field("secret", env="ADMIN_SECRET")
    admin_username: str = Field("admin", env="ADMIN_USERNAME")
    admin_password_hash: SecretStr = Field("admin", env="ADMIN_PASSWORD")


settings = Settings()
