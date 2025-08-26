from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.category import Category, CategoryCreate
from app.services import category as category_service

router = APIRouter()


@router.get("/categories")
def read_categories(
    db: Annotated[Session, Depends(get_db)], skip: int = 0, limit: int = 100
) -> list[Category]:
    """Get categories with pagination."""
    db_categories = category_service.get_categories(db, skip=skip, limit=limit)

    return [Category.model_config(db_cat) for db_cat in db_categories]  # pyright: ignore[reportCallIssue]


@router.post("/", response_model=Category)
def create_category(
    category: CategoryCreate, db: Annotated[Session, Depends(get_db)]
) -> category_service.CategoryModel:
    """Create a new category."""
    existing = category_service.get_category_by_name(db, category.name)
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")
    return category_service.create_category(db=db, category=category)
