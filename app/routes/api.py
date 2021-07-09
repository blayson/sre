from fastapi import APIRouter

from app.routes import auth, users, admin, reviews

router = APIRouter()

router.include_router(auth.router, tags=["auth"], prefix="/auth")
router.include_router(users.router, tags=["users"], prefix="/users")
router.include_router(admin.router, tags=["admin"], prefix="/admin")
router.include_router(reviews.router, tags=["reviews"], prefix="/reviews")
# router.include_router(profiles.router, tags=["profiles"], prefix="/profiles")
# router.include_router(articles.router, tags=["articles"])
# router.include_router(
#     comments.router,
#     tags=["comments"],
#     prefix="/articles/{slug}/comments",
# )
# router.include_router(tags.router, tags=["tags"], prefix="/tags")
