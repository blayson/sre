from enum import Enum


class BaseEnum(Enum):
    def __str__(self):
        return f"{self.name}".lower().capitalize()


class UserReviewState(Enum):
    REVIEWED = "reviewed"
    NOT_REVIEWED = "notReviewed"
    APPROVED = "approved"
    REJECTED = "rejected"


class LanguagesQueryParameter(Enum):
    CZECH = "czech"
    ENGLISH = "english"
    GERMAN = "german"


class UserRoles(Enum):
    ADMIN = "admin"
    USER = "user"


USER_ROLES_MAP = {UserRoles.USER: 1, UserRoles.ADMIN: 2}


