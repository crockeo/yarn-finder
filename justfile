set positional-arguments

dev:
    uv run python -m yarn_finder.main

upgrade:
    uv run python -m alembic upgrade HEAD

downgrade:
    uv run python -m alembic downgrade -1

[positional-arguments]
revision message:
    uv run python -m alembic revision --autogenerate -m "{{ message }}"
