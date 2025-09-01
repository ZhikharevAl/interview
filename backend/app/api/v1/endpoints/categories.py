from typing import Annotated, Any

from app.db.database import get_db
from app.schemas.category import Category, CategoryCreate, CategoryDelete
from app.services import category as category_service
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/")
def read_categories(
    db: Annotated[Session, Depends(get_db)],
    skip: int = 0,
    limit: int = 100,
) -> list[Category]:
    """Get categories."""
    db_categories = category_service.get_categories(db, skip=skip, limit=limit)
    return [Category.model_validate(db_cat) for db_cat in db_categories]


@router.get("/{category_id}")
def read_category(category_id: int, db: Annotated[Session, Depends(get_db)]) -> Category:
    """Get category by ID."""
    db_category = category_service.get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return Category.model_validate(db_category)


@router.post("/", response_model=Category)
def create_category(
    category: CategoryCreate, db: Annotated[Session, Depends(get_db)]
) -> category_service.CategoryModel:
    """Create a new category."""
    existing = category_service.get_category_by_name(db, category.name)
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")
    return category_service.create_category(db=db, category=category)


@router.delete("/{category_id}", response_model=CategoryDelete)
def delete_category(category_id: int, db: Annotated[Session, Depends(get_db)]) -> dict[str, Any]:
    """Delete a category by ID."""
    deleted = category_service.delete_category(db, category_id=category_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"id": category_id, "deleted": True}
