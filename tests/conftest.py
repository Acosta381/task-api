import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from core.limiter import limiter
from database import Base, get_db
from main import app

limiter.enabled = False

TEST_DATABASE_URL = 'postgresql+asyncpg://postgres:1234@localhost:5432/taskdb_test'


test_engine = create_async_engine(TEST_DATABASE_URL, poolclass = NullPool)

TestSessionLocal = async_sessionmaker(test_engine, expire_on_commit=False)

@pytest.fixture
async def db_session():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestSessionLocal() as session:
        yield session

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def client(db_session):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url='http://test'
    ) as ac:
        yield ac

    app.dependency_overrides.clear()