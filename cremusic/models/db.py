from datetime import datetime
from sqlalchemy import ForeignKey, create_engine, String
from sqlalchemy.orm import sessionmaker, mapped_column, Mapped, DeclarativeBase
from sqlalchemy.orm import MappedAsDataclass

from cremusic.utils import now

# DATABASE_URL = "postgresql://user:password@postgresserver/db"
DATABASE_URL = "sqlite:///./cremusic.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(
    MappedAsDataclass,
    DeclarativeBase,
):
    pass


class BookCodeConfig(Base):
    __tablename__ = "config"
    id: Mapped[int] = mapped_column(primary_key=True)
    required_unlock: Mapped[bool]
    global_code: Mapped[str]
    secret: Mapped[str]
    test: Mapped[str]



class BookCode(Base):
    __tablename__ = "book_code"
    id: Mapped[int] = mapped_column(primary_key=True)
    serial: Mapped[str] = mapped_column(unique=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"))
    code: Mapped[str] = mapped_column(unique=True)
    release_version: Mapped[str]


class Book(Base):
    __tablename__ = "book"
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(32))
    name: Mapped[str] = mapped_column(String(256))
    background_image_url: Mapped[str] = mapped_column(String(1024))
    background_color_code: Mapped[str]

    created_by: Mapped[str] = mapped_column(String(256), default="system")
    created_date: Mapped[datetime] = mapped_column(
        default_factory=now
    )

    modified_by: Mapped[str] = mapped_column(String(256), default="system")
    modified_date: Mapped[datetime] = mapped_column(
        default_factory=now
    )


class Episode(Base):
    __tablename__ = "book_episode"
    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"))

    name: Mapped[str | None] = mapped_column(String(256))
    author: Mapped[str | None] = mapped_column(String(256), default="")
    artist: Mapped[str | None] = mapped_column(String(256), default="")
    background_image_url: Mapped[str | None] = mapped_column(
        String(1024),
        default=None
    )
    background_color_code: Mapped[int | None] = mapped_column(default=None)

    created_by: Mapped[str] = mapped_column(String(256), default="system")
    created_date: Mapped[datetime] = mapped_column(
        default_factory=now
    )

    modified_by: Mapped[str] = mapped_column(String(256), default="system")
    modified_date: Mapped[datetime] = mapped_column(
        default_factory=now
    )


# class Pokemon(Base):
#     __tablename__ = "pokemon"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(String(256))
#     type: Mapped[str] = mapped_column(String(256))
#     created_by: Mapped[str] = mapped_column(String(256))
#     created_date: Mapped[datetime] = mapped_column()
#     modified_by: Mapped[str] = mapped_column(String(256))
#     modified_date: Mapped[datetime] = mapped_column(
#         default_factory=now
#     )


class StatisticLog(Base):
    __tablename__  = "statistic_log"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(256))
    email: Mapped[str | None] = mapped_column(String(256))
    code: Mapped[str] = mapped_column(String(64))
    telephone: Mapped[str] = mapped_column(String(16))


class Video(Base):
    __tablename__ = "book_episode_video"
    id: Mapped[int] = mapped_column(primary_key=True)
    book_episode_id: Mapped[int] = mapped_column(ForeignKey("book_episode.id"))
    video_id: Mapped[str] = mapped_column(String(64))

    name: Mapped[str | None] = mapped_column(String(1024))
    link: Mapped[str | None] = mapped_column(String(1024))
    thumbnail: Mapped[str | None] = mapped_column(String(1024))
    duration: Mapped[int] = mapped_column(default=0)

