from app.core.db import Base


class UsersTable(Base):
    __tablename__ = 'users'


class UserRolesTable(Base):
    __tablename__ = 'user_roles'


class ReviewsTable(Base):
    __tablename__ = 'reviews'


class ProductsTable(Base):
    __tablename__ = 'reviews'


TUsers = UsersTable.__table__
TUserRoles = UserRolesTable.__table__
TReviews = ReviewsTable.__table__
TProducts = ProductsTable.__table__
