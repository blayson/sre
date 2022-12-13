from enum import Enum


class UserReviewState(Enum):
    REVIEWED = "reviewed"
    NOT_REVIEWED = "notReviewed"
    APPROVED = "approved"
    REJECTED = "rejected"
