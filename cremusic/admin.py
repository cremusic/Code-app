from pathlib import Path
from fastapi import Request
from sqladmin.authentication import AuthenticationBackend
from starlette.responses import RedirectResponse
from sqladmin import Admin, ModelView, action
from passlib.hash import pbkdf2_sha256

from sqladmin import ModelView, action, expose, BaseView
from fastapi import Request, Form
from sqlalchemy.ext.asyncio import AsyncSession

from cremusic.app import app
from cremusic.db import engine, SessionLocal, autocommit
from cremusic.config import settings
from cremusic.models.db import (
    Book, BookCode, BookCodeConfig, Episode, StatisticLog, Video
)
from cremusic.generator import BookCodeGenerator


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


BASE_DIR = Path(__file__).resolve().parent


admin = Admin(
    app, engine, authentication_backend=authentication_backend,
    templates_dir=str(Path(BASE_DIR, 'templates'))
)


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

    @action(
        name="generate_codes",
        label="Generate Codes",
    )
    async def generate_codes(self, request: Request):
        """
        Custom action to generate multiple codes for selected books.
        """
        pks_query = request.query_params.get("pks", "")
        if not pks_query:
            return RedirectResponse(url="/admin/book/list")
        return RedirectResponse(
            url=f"/admin/book/generate_codes?pks={pks_query}",
            status_code=302,
        )


@register()
class EpisodeAdmin(ModelView, model=Episode):
    column_exclude_list = ['videos']
    column_details_exclude_list = ['videos']
    column_searchable_list = (
        Episode.name,
        Episode.book_id,
        Episode.artist,
        Episode.author,
    )
    form_excluded_columns = ['videos']


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
    column_default_sort = ("id", True)
    column_searchable_list = (
        BookCode.code,
    )


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


@register()
class GeneratorCodeView(BaseView):
    include_in_schema = False

    @expose("/book/generate_codes", methods=["GET", "POST"])
    async def report_page(self, request):
        if request.method == "POST":
            form = await request.form()
            book_ids = form.get("book_ids", "").split(",")
            num_codes = int(form.get("num_codes", 0))
            version = form.get("version", "")
            with SessionLocal() as db:
                with autocommit(db):
                    book_code_generator = BookCodeGenerator(
                        db=db
                    )
                    print(f"Generating codes for books: {book_ids}")
                    for book_id in book_ids:
                        book_code_generator.generate_code(
                            quantity=num_codes,
                            book_id=book_id,
                            version=version
                        )
            return RedirectResponse(
                url="/admin/book-code/list", status_code=302
            )

        pks_query = request.query_params.get("pks", "")
        if not pks_query:
            return RedirectResponse(
                url="/admin/book/list", status_code=302
            )
            
        return self.templates.TemplateResponse(
            "code_generator.html",
            context={
                "request": request,
                "book_ids": pks_query
            }
        )
