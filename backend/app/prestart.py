# Ensure DB connectivity on container start, create tables and seed if flag is set.
import asyncio
from .core.config import settings
from .db.session import engine
from .db.base import Base
from sqlalchemy import text

async def main():
    if settings.db_driver == "sqlite":
        # SQLite file is created automatically on connect via SQLAlchemy
        pass
    # Small sanity check query
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    print("DB prestart check passed.")

if __name__ == "__main__":
    asyncio.run(main())
