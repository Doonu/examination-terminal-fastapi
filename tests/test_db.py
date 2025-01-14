from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from core.config import settings
from core.models import Base

TEST_DB_URL = settings.db.url

test_engine = create_async_engine(TEST_DB_URL, echo=True)
TestSessionLocal = async_sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


async def get_test_db() -> AsyncSession:
    async with TestSessionLocal() as session:
        yield session


async def create_test_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
