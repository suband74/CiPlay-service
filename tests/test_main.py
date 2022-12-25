import pytest
from httpx import AsyncClient
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine

from ciplay_service.main import app
from ciplay_service.settings import get_session, POSTGRES_DATABASE_URL


@pytest.fixture
def anyio_backend():
    return 'asyncio'

@pytest.mark.anyio
async def test_create_event():
    engine = create_async_engine(POSTGRES_DATABASE_URL, connect_args={"check_same_thread": False})
    app.dependency_overrides[get_session] = lambda: get_session()

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post(
                "/event",
                json={"name": "TestGuy", "password": "TestPass"},
            )
            assert response.status_code == 200, response.text
