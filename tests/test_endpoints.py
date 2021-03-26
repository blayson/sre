import os

from openapi_spec_validator import validate_spec_url


def test_swagger_specification(host):
    endpoint = os.path.join(host, 'routes', 'swagger.json')
    validate_spec_url(endpoint)
