from datetime import datetime
from sqlalchemy import ForeignKey, SmallInteger, String, UniqueConstraint, BigInteger
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import func

from cremusic.db import Base


class _Common:
    id: Mapped[int] = mapped_column(BigInteger(), primary_key=True)


class Book(_Common, Base):
    __tablename__ = "book"
    type: Mapped[str | None] = mapped_column(String(32), nullable=True)
    name: Mapped[str | None] = mapped_column(String(256), nullable=True)
    background_image_url: Mapped[str | None] = mapped_column(
        String(1024), default=None, nullable=True
    )
    background_color_code: Mapped[int | None] = mapped_column(
        SmallInteger(), default=None, nullable=True
    )
    created_date: Mapped[datetime] = mapped_column(
        server_default=func.now()
    )
    created_by: Mapped[str] = mapped_column(String(256), server_default="system")
    modified_by: Mapped[str | None] = mapped_column(
        String(256), nullable=True, default=None
    )
    modified_date: Mapped[datetime | None] = mapped_column(
        nullable=True, default=None
    )
    not_require_unlock: Mapped[bool | None] = mapped_column(nullable=True, default=None)

    def __str__(self) -> str:
        return f"{self.id} - {self.name}"


class BookCodeConfig(_Common, Base):
    __tablename__ = "config"
    required_unlock: Mapped[bool | None] = mapped_column(nullable=True, default=None)
    global_code: Mapped[str | None] = mapped_column(
        String(250),
        nullable=True,
        default=None
    )
    secret: Mapped[str] = mapped_column(String(250), nullable=True, default=None)


class BookCode(_Common, Base):
    __tablename__ = "book_code"
    serial: Mapped[str] = mapped_column(String(64), unique=True)
    book_id: Mapped[int] = mapped_column(BigInteger(), ForeignKey("book.id"))
    code: Mapped[str] = mapped_column(String(64), unique=True)
    release_version: Mapped[str] = mapped_column(String(64))


class Episode(_Common, Base):
    __tablename__ = "book_episode"
    book_id: Mapped[int] = mapped_column(BigInteger(), ForeignKey("book.id"))
    book: Mapped[Book] = relationship("Book", backref="episodes")
    name: Mapped[str | None] = mapped_column(String(256))
    author: Mapped[str | None] = mapped_column(String(256), server_default="")
    artist: Mapped[str | None] = mapped_column(String(256), server_default="")
    background_image_url: Mapped[str | None] = mapped_column(
        String(1024),
        default=None
    )
    background_color_code: Mapped[int | None] = mapped_column(default=None)

    created_by: Mapped[str] = mapped_column(String(128), server_default="system")
    created_date: Mapped[datetime] = mapped_column(server_default=func.now())

    modified_by: Mapped[str | None] = mapped_column(
        String(128),
        nullable=True,
        default=None
    )
    modified_date: Mapped[datetime | None] = mapped_column(nullable=True, default=None)

    def __str__(self):
        return f"{self.id} - {self.name} (book {self.book_id})"


class StatisticLog(_Common, Base):
    __tablename__  = "statistic_log"
    __table_args__ = (
        UniqueConstraint("telephone", "code"),
    )
    name: Mapped[str] = mapped_column(String(256))
    code: Mapped[str] = mapped_column(String(64))
    telephone: Mapped[str] = mapped_column(String(16))
    email: Mapped[str | None] = mapped_column(String(256), nullable=True, default=None)


class Video(_Common, Base):
    __tablename__ = "book_episode_video"
    book_episode_id: Mapped[int] = mapped_column(
        BigInteger(),
        ForeignKey("book_episode.id")
    )
    episode = relationship("Episode", backref="videos")
    video_id: Mapped[str] = mapped_column(String(64))

    name: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    link: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    thumbnail: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    duration: Mapped[int] = mapped_column(
        BigInteger(),
        nullable=True,
        server_default="0"
    )

    def __str__(self):
        return f"{self.id} - {self.name} (episode {self.book_episode_id})"
