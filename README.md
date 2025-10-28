# Budgeteer — Dockerized Personal Budgeting App

> Modern FastAPI + React budgeting app with JWT auth, split transactions, budgets, reports, CSV import, and persistent Docker volumes.

## Quick Start

```bash
git clone <this-repo> budgeteer
cd budgeteer
cp .env.example .env
docker compose up -d --build
# API: http://localhost:8000/api/v1/docs  (dev)
# Web: http://localhost:8080
```

If Postgres isn't available, set `DB_DRIVER=sqlite` in `.env` (dev only).

## Volumes
- `db-data` — PostgreSQL data
- `app-media` — Uploaded files (attachments)
- `pg-backups` — Database dumps created by `make backup`

## Makefile Cheatsheet
```bash
make up        # build & run all
make down      # stop
make logs      # tail compose logs
make format    # ruff/black + eslint/prettier
make lint      # back & front
make test      # pytest + vitest
make seed      # seed demo data
make migrate   # autogenerate & apply alembic
make backup    # pg_dump to ./backups
make restore   # psql restore from latest
```

## Architecture (Mermaid)
```mermaid
flowchart LR
  subgraph Web[Frontend: React/Vite]
    Pages-->APIClient
    APIClient-->JWTStorage
  end

  subgraph API[Backend: FastAPI]
    Routers-->Services-->DB[(SQLAlchemy)]
    Routers-->Security[JWT/Argon2/TOTP]
    Routers-->Media[(Attachments Volume)]
    API<-->OpenAPI
  end

  Web<-->API
  DB[(Postgres Volume)]---API
  Media[(app-media)]---API
```

## Production Notes
- Put a reverse proxy (nginx/traefik) in front of `web` and `api` with TLS.
- Rotate JWT secrets periodically.
- Configure off-site backups: copy `pg-backups` to S3/Backblaze/etc.
- Set strict `CORS_ORIGINS` to your prod domain.
- Disable Swagger via `API_ENV=production` or admin toggle.

See `docs/` for details.
