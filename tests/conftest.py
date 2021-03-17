import pytest
import os
import sys


sys.path.append('..')
from config import TestConfig
from app import DB, create_app
from app.models import User


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
#     return os.path.join(host, "api", "v1")


@pytest.fixture(scope='function')
def app():
    _app = create_app(TestConfig)
    ctx = _app.test_request_context()
    ctx.push()

    DB.drop_all()
    DB.create_all()

    yield _app

    DB.session.remove()
    DB.drop_all()
    ctx.pop()


@pytest.fixture(scope='function')
def user(app):
    user = User(email='test@test.com', password='password')
    DB.session.add(user)
    DB.session.commit()

    return user
