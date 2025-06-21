"""
Runs the asynchronous `init_models` function using asyncio.

Typically executed by developers using `just migrate` command
to apply schema migrations during development.
"""

import asyncio

from src.db.database import engine
from src.db.models import Base


async def init_models() -> None:
    """
    Create all database tables defined in the ORM models.

    Uses the async engine to establish a connection and runs the
    synchronous `create_all` method on the metadata within the async context.

    This function initializes the database schema according to the models.

    Note:
        This script is intended to be run manually by developers to
        initialize or migrate the database schema during development.
        It is executed via the `just migrate` command.

        It is not part of the production runtime flow.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(init_models())
