from app.core.db import Base


class UsersTable(Base):
    __tablename__ = 'users'


class UserRolesTable(Base):
    __tablename__ = 'user_roles'


class ReviewsTable(Base):
    __tablename__ = 'reviews'


TUsers = UsersTable.__table__
UserRoles = UserRolesTable.__table__
Reviews = ReviewsTable.__table__
