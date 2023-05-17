from sqlmodel import Session, create_engine
from cremusic.config import settings

engine = create_engine(
    f"postgresql://{settings.pg_user}:{settings.pg_password.get_secret_value()}@{settings.pg_host}",
    echo=True
)


def get_session():
    with Session(engine) as session:
        yield session
