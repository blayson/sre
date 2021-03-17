from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin

from app.schemas import *

# Create an APISpec
spec = APISpec(title="Semantic evaluator",
               version="1.0.0",
               openapi_version="3.0.2",
               plugins=[FlaskPlugin(), MarshmallowPlugin()])

# register security scheme
jwt_scheme = {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
spec.components.security_scheme("jwt", jwt_scheme)

# register schemas with spec
spec.components.schema("Review", schema=ReviewSchema)
spec.components.schema("Register", schema=RegisterSchema)
spec.components.schema("User", schema=UserSchema)
spec.components.schema("Auth", schema=AuthSchema)
