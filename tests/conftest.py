from typing import Generator

import databases
import pytest
import sys
import contextlib

# sys.path.append('..')
#
# from conf.config import TestConfig
# from app import DB, create_app
# from app.models.domain import Users
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.main import create_application
from app.settings import settings
from app.utils.db import get_db


async def get_db_override():
    db = databases.Database(settings.database_url, force_rollback=True)
    await db.connect()
    yield db
    await db.disconnect()


@pytest.fixture(scope="function")
def test_client_with_db() -> Generator:
    # set up
    app = create_application()
    app.dependency_overrides[get_db] = get_db_override

    with TestClient(app) as test_client_with_db:
        yield test_client_with_db


# @pytest.fixture(scope="function")
# async def test_async_client_with_db() -> Generator:
#     # set up
#     app = create_application()
#     app.dependency_overrides[get_db] = get_db_override
#
#     async with AsyncClient(app=app, base_url='http://localhost:8000') as test_client_with_db:
#         # testing
#         yield test_client_with_db


# def pytest_addoption(parser):
#     # ability to test API on different hosts
#     parser.addoption("--host", action="store", default="http://localhost:5000")
#
#
# @pytest.fixture(scope="session")
# def host(request):
#     return request.config.getoption("--host")
#
#
# @pytest.fixture(scope="session")
# def api_v1_host(host):
#     return os.path.join(host, "routes", "v1")


# @pytest.fixture(scope='function')
# def app():
#     app = create_app(TestConfig)
#     ctx = app.test_request_context()
#     ctx.push()
#
#     DB.drop_all()
#     DB.create_all()
#
#     yield app
#
#     DB.session.remove()
#
#     with contextlib.closing(DB.engine.connect()) as con:
#         trans = con.begin()
#         for table in reversed(DB.metadata.sorted_tables):
#             con.execute(table.delete())
#         trans.commit()
#
#     ctx.pop()
#
#
# @pytest.fixture(scope='function')
# def user(app):
#     user = Users(email='test@test.com', password='password')
#     DB.session.add(user)
#     DB.session.commit()
#
#     return user
