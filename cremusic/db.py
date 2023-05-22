from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, Session, sessionmaker
from cremusic.config import settings


DATABASE_URL = f"postgresql://{settings.pg_user}:{settings.pg_password.get_secret_value()}@{settings.pg_host}/{settings.pg_dbname}"  # noqa
# DATABASE_URL = "sqlite:///./cremusic.db"

engine = create_engine(
    DATABASE_URL,
    # connect_args={"check_same_thread": False},
    echo=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    # with Session(engine) as session:
    #     yield session
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Base(
    MappedAsDataclass,
    DeclarativeBase,
):
    pass
