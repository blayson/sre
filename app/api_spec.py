from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin

from app.schemas import *

# Create an APISpec
spec = APISpec(
    title="Semantic evaluator",
    version="1.0.0",
    openapi_version="3.0.2",
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)

# register schemas with spec
spec.components.schema("Review", schema=ReviewSchema)
spec.components.schema("Register", schema=RegisterSchema)
spec.components.schema("User", schema=UserSchema)
spec.components.schema("Auth", schema=AuthSchema)

# add swagger tags that are used for endpoint annotation
tags = [
    {'name': 'Auth',
     'description': 'Auth module'},
    {'name': 'User',
     'description': 'User module'},
]

for tag in tags:
    # print(f"Adding tag: {tag['name']}")
    spec.tag(tag)
