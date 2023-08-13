from fastapi import Request
from sqladmin.authentication import AuthenticationBackend
from starlette.responses import RedirectResponse
from sqladmin import Admin, ModelView
from passlib.hash import pbkdf2_sha256

from cremusic.app import app
from cremusic.db import engine
from cremusic.config import settings
from cremusic.models.db import (
    Book, BookCode, BookCodeConfig, Episode, StatisticLog, Video
)


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]
        if username != settings.admin_username:
            return False
        try:
            pwd_valid = pbkdf2_sha256.verify(
                password,
                settings.admin_password_hash.get_secret_value()
            )
        except ValueError:
            return False
        if not pwd_valid:
            return False

        # Validate username/password credentials
        # And update session
        request.session.update({"token": "logged_in"})

        return True

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> RedirectResponse | None:
        token = request.session.get("token")

        if not token:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)

        # Check the token in depth
        if token != "logged_in":
            return RedirectResponse(request.url_for("admin:login"), status_code=302)


authentication_backend = AdminAuth(
    secret_key=settings.admin_secret_key.get_secret_value()
)

admin = Admin(app, engine, authentication_backend=authentication_backend)


def register():
    """Decorator that adds a model to the admin interface."""
    def decorator(cls):
        admin.add_view(cls)
        return cls

    return decorator


@register()
class BookAdmin(ModelView, model=Book):
    column_exclude_list = ["episodes"]
    column_details_list = "__all__"
    form_excluded_columns = [
        "episodes", "modified_date", "modified_by", "created_date", "created_by"
    ]
    column_searchable_list = (
        Book.name,
    )


@register()
class EpisodeAdmin(ModelView, model=Episode):
    column_list = "__all__"
    column_details_list = "__all__"
    column_searchable_list = (
        Episode.name,
        Episode.book_id,
        Episode.artist,
        Episode.author,
    )


@register()
class VideoAdmin(ModelView, model=Video):
    column_list = "__all__"
    column_details_list = "__all__"
    column_searchable_list = (
        Video.name,
        Video.link,
    )


@register()
class CodeConfigAdmin(ModelView, model=BookCodeConfig):
    column_list = "__all__"
    column_details_list = "__all__"


@register()
class CodeAdmin(ModelView, model=BookCode):
    column_list = "__all__"
    column_details_list = "__all__"


@register()
class StatisticLogAdmin(ModelView, model=StatisticLog):
    column_list = "__all__"
    column_details_list = "__all__"
    column_searchable_list = (
        StatisticLog.code,
        StatisticLog.email,
        StatisticLog.name,
        StatisticLog.telephone,
    )
    column_default_sort = ("id", True)
