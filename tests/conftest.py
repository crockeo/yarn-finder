import tempfile
from pathlib import Path
from typing import Generator

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from yarn_finder import database


@pytest.fixture
def tmp_path() -> Generator[Path, None, None]:
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)


@pytest_asyncio.fixture
async def engine(tmp_path: Path) -> AsyncEngine:
    _engine = create_async_engine(f"sqlite+aiosqlite:///{tmp_path}")
    await database.create_schema(_engine)
    return _engine


@pytest_asyncio.fixture
async def sess(engine: AsyncEngine):
    async with database.create_session(engine) as _sess:
        yield _sess
