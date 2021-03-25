import pytest
import sys
import contextlib

sys.path.append('..')

# from conf.config import TestConfig
# from app import DB, create_app
# from app.models.domain import Users


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
