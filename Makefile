SHELL := /bin/bash

up:
	docker compose up -d --build

down:
	docker compose down

logs:
	docker compose logs -f --tail=200

format:
	cd backend && ruff check --fix . && black .
	cd frontend && pnpm prettier --write . && pnpm eslint . --fix || true

lint:
	cd backend && ruff check . && black --check .
	cd frontend && pnpm eslint .

test:
	cd backend && pytest -q
	cd frontend && pnpm test -- --run

seed:
	docker compose exec api python -m app.scripts.seed

migrate:
	cd backend && alembic revision --autogenerate -m "auto" && alembic upgrade head

backup:
	docker compose exec db bash -lc 'pg_dump -U $$POSTGRES_USER $$POSTGRES_DB > /backups/backup-$$(date +%F_%H%M%S).sql'

restore:
	docker compose exec db bash -lc 'psql -U $$POSTGRES_USER $$POSTGRES_DB < $$(ls -t /backups/*.sql | head -n1)'
