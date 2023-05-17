# cremusic backend project

- Python 3.11
- FastAPI REST API
  - Auto generated api doc

- Postgrest database with SQLAlchemy ORM
- Alembic for db migrations
- Docker/docker compose deployment

## Alembic

Alembic basic usage would be: create new revision then run upgrade. Creating
revision with `--autogenerate` option will detect table model changes versus
current database tables.

- Create new revision `alembic revision --autogenerate -m "message"`
- Run migration `alembic upgrade head`
