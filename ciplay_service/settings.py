import os
from sqlmodel import SQLModel
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


load_dotenv()

USER = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
DATABASE = os.getenv("POSTGRES_DB")
HOST = os.getenv("POSTGRES_SERVER")

POSTGRES_DATABASE_URL = f"postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:5432/{DATABASE}"

engine = create_async_engine(POSTGRES_DATABASE_URL, echo=True, future=True)


async def get_session() -> AsyncSession:
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
