from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from cremusic.config import settings


DATABASE_URL = f"postgresql://{settings.pg_user}:{settings.pg_password.get_secret_value()}@{settings.pg_host}/{settings.pg_dbname}"  # noqa

engine = create_engine(
    DATABASE_URL,
    echo=True if settings.debug else False
)
SessionLocal = sessionmaker(
    autoflush=True,
    bind=engine
)


def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def autocommit(ses: Session):
    """Context manager that commits on exit, rolls back on exception."""
    try:
        yield ses
        ses.commit()
    except Exception:
        ses.rollback()
        raise


class Base(DeclarativeBase):
    pass
