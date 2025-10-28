# Setup & Troubleshooting

- Ensure Docker & Docker Compose are installed.
- Copy `.env.example` to `.env` and adjust origins, secrets.
- Ports used: 5432 (db), 8000 (api), 8080 (web). Change via `.env`.
- File permissions: Docker volumes handle persistence; attachments live in `app-media`.

## Migrations
`make migrate` will autogenerate and apply Alembic migrations from models.

## Backups
`make backup` creates dumps in `pg-backups` volume. Copy them out regularly.
