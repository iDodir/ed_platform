# import asyncio
# import os
# from typing import Generator, Any, AsyncGenerator
#
# import asyncpg
# import pytest
# from fastapi.testclient import TestClient
# from httpx import AsyncClient
# from sqlalchemy import text
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy.orm import sessionmaker
#
# import settings
# from db.models import Base
# from db.session import get_db
# from main import app
#
# test_engine = create_async_engine(settings.TEST_DATABASE_URL, future=True, echo=True)
# test_async_session = sessionmaker(test_engine, expire_on_commit=False, class_=AsyncSession)
# Base.metadata.bind = test_engine
#
#
# async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
#     async with test_async_session() as session:
#         yield session
#
#
# app.dependency_overrides[get_db] = override_get_db
#
#
# @pytest.fixture(autouse=True, scope="session")
# async def prepare_database():
#     async with test_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     yield
#     async with test_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#
#
# @pytest.fixture(scope="session")
# def event_loop(request):
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()
#
#
# client = TestClient(app)
#
#
# @pytest.fixture(scope="session")
# async def asyncpg_pool():
#     pool = await asyncpg.create_pool("".join(settings.TEST_DATABASE_URL.split("+asyncpg")))
#     yield pool
#     pool.close()
#
#
# @pytest.fixture
# async def get_user_from_database(asyncpg_pool):
#
#     async def get_user_from_database_by_uuid(user_id: str):
#         async with asyncpg_pool.acquire() as connection:
#             return await connection.fetch("""SELECT * FROM users WHERE user_id = $1;""", user_id)
#
#     return get_user_from_database_by_uuid
