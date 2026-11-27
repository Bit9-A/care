# AGENTS.md — CARE backend

Django backend of **CARE** (open source EMR + hospital management, Digital Public Good).
Django 6.0 · Python **3.13 (strict)** · PostgreSQL 16 · Redis · Celery · Pipenv.

`CLAUDE.md` in this repo carries the detailed upstream guidance — read it for architecture
depth. This file is the entry point for agents that read `AGENTS.md`.

## Structure

```
care/            # main Django app: emr/ facility/ users/ security/ audit_log/ utils/
config/          # settings (base, local, test, deployment), api_router.py, celery_app.py
plugs/           # plugin system (manager + Plug dataclass)
plug_config.py   # ← the only place features are declared
```

API: DRF + `drf-nested-routers`, JWT via `simplejwt`, OpenAPI via `drf-spectacular`, routes in
`config/api_router.py`.

## Commands

Docker (preferred):

| Task | Command |
|---|---|
| setup | `cp .env.example .env` |
| start (db, redis, minio, backend, celery) | `make up` |
| migrate | `make migrate` |
| new migration | `make makemigrations` |
| fixtures | `make load-fixtures` |
| **focused test** | `make test path="care.users"` |
| full suite (only before delivery) | `make test` |
| lint + format | `make ruff-fix-all` |
| logs / stop | `make logs` / `make down` |

Pipenv (local venv + native Postgres/Redis):

```bash
pipenv run python manage.py migrate
pipenv run python manage.py test care.users --keepdb --parallel
pipenv run ruff check --fix . && pipenv run ruff format .
```

`DJANGO_SETTINGS_MODULE=config.settings.local` for local runs; `config.settings.test` for tests.

## Rules

- **Features go in a plugin, never in the core.** Declare a `Plug(...)` in `plug_config.py`
  (`plug_config.py` > env vars > plugin defaults); its URLs mount at `/api/<plugin-name>/`.
  When touching core models or API, check the plugin interfaces first.
- **Do not hand-edit migrations.** `make makemigrations` then `make migrate`.
- **Do not run the full suite for a narrow change.** `make test path="care.<app>"`.
- **Do not commit `.env`** or fixtures with real patient data.
- **Python 3.13.x only** (`requires-python == "3.13.*"`).

## Skills pack (OpenCode)

Active: `core python` — re-activate with `skills-pack on core python` from this directory.
`.opencode/skills/` is machine-local and gitignored.
