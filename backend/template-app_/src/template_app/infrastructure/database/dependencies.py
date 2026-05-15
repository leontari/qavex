from collections.abc import AsyncGenerator
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession


async def get_session(
    request: Request,
) -> AsyncGenerator[AsyncSession, None]:

    session_factory = request.app.state.session_factory

    async with session_factory() as session:
        try:
            yield session
            await session.commit()

        except Exception:
            await session.rollback()
            raise
