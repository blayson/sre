from fastapi import APIRouter

from app.routes import auth, users, admin, reviews, suggestions

router = APIRouter()

router.include_router(auth.router, tags=["auth"], prefix="/auth")
router.include_router(users.router, tags=["users"], prefix="/users")
router.include_router(admin.router, tags=["admin"], prefix="/admin")
router.include_router(reviews.router, tags=["reviews"], prefix="/reviews")
router.include_router(suggestions.router, tags=["suggestions"], prefix="/suggestions")
