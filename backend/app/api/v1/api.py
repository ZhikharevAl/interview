from app.api.v1.endpoints import categories, questions
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(questions.router, prefix="/questions", tags=["questions"])
