import databases
import pytest
from fastapi.testclient import TestClient

from app.models.domain.tables import users
from app.models.schemas.auth import Token
from app.models.schemas.users import UserInRegister, User
from app.services.users import UsersService
from app.settings import settings

TEST_USER = {'name': 'test_user',
             'email': 'test@test.com',
             'password': '12345'}


def test_register(test_client_with_db: TestClient):
    response = test_client_with_db.post('/api/v1/auth/register', json=TEST_USER)
    data = response.json()
    assert response.status_code == 201
    assert Token.validate(data)


@pytest.mark.asyncio
async def test_create_user():
    async with databases.Database(settings.database_url, force_rollback=True) as db:
        user = await UsersService(db).create_user(UserInRegister(name=TEST_USER['name'],
                                                                 email=TEST_USER['email'],
                                                                 password=TEST_USER['password']))
        query = users.select().where(TEST_USER['email'] == users.c.email)
        db_user = await db.fetch_one(query)
        assert User(**user) == User(**db_user)

# from openapi_spec_validator import validate_spec_url
#
#
# def test_swagger_specification(host):
#     endpoint = os.path.join(host, 'routes', 'swagger.json')
#     validate_spec_url(endpoint)
#
