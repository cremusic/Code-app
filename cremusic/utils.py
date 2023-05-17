from datetime import datetime
from cremusic.config import settings


def now() -> datetime:
    return datetime.now(tz=settings.tz)
