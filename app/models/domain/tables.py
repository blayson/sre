from sqlalchemy import Table

from app.utils.db import metadata

products = Table(
    "products",
    metadata,
)

product_names = Table(
    "product_names",
    metadata,
)

product_categories = Table("product_categories", metadata)

product_category_names = Table("product_category_names", metadata)

reviews = Table(
    "reviews",
    metadata,
)

product_features_keywords = Table(
    "product_features_keywords",
    metadata,
)

feature_names = Table(
    "feature_names",
    metadata,
)

users = Table(
    "users",
    metadata,
)

user_roles = Table(
    "user_roles",
    metadata,
)

reviews_suggestions = Table("reviews_suggestions", metadata)

reviews_suggestions_states = Table("reviews_suggestions_states", metadata)
