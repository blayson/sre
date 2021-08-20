from sqlalchemy import Table

from app.core.db import metadata

products = Table(
    "products",
    metadata,
)

reviews = Table(
    "reviews",
    metadata,
)

product_names = Table(
    "product_names",
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

#
# class UsersTable(Base):
#     __tablename__ = 'users'
#
#
# class UserRolesTable(Base):
#     __tablename__ = 'user_roles'

#
# class ReviewsTable(Base):
#     __tablename__ = 'reviews'
#
#
# class ProductsTable(Base):
#     __tablename__ = 'products'
#
#
# class ProductNames(Base):
#     __tablename__ = 'product_names'
#
#
# class FeatureNames(Base):
#     __tablename__ = 'feature_names'
#
#
# class ProductsFeaturesKeywords(Base):
#     __tablename__ = 'product_features_keywords'
#
#
# TUsers = UsersTable.__table__
# TUserRoles = UserRolesTable.__table__
# TReviews = ReviewsTable.__table__
# TProducts = ProductsTable.__table__
# TProductNames = ProductNames.__table__
# TFeatureNames = FeatureNames.__table__
# TProductsFeaturesKeywords = ProductsFeaturesKeywords.__table__
