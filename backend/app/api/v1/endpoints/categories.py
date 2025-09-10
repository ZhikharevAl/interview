from typing import Annotated, Any

from app.db.database import get_db
from app.schemas.category import Category, CategoryCreate, CategoryDelete, CategoryUpdate
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


@router.post("/", response_model=Category, status_code=201)
def create_category(
    category: CategoryCreate, db: Annotated[Session, Depends(get_db)]
) -> category_service.CategoryModel:
    """Create a new category."""
    existing = category_service.get_category_by_name(db, category.name)
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Category '{category.name}' already exists (found '{existing.name}')",
        )
    return category_service.create_category(db=db, category=category)


@router.put("/{category_id}", response_model=Category)
def update_category(
    category_id: int, category: CategoryUpdate, db: Annotated[Session, Depends(get_db)]
) -> category_service.CategoryModel:
    """Update a category by ID."""
    existing_category = category_service.get_category(db, category_id=category_id)
    if not existing_category:
        raise HTTPException(status_code=404, detail="Category not found")

    if category.name and category.name.lower() != existing_category.name.lower():
        existing_name = category_service.get_category_by_name(db, category.name)
        if existing_name:
            raise HTTPException(
                status_code=400,
                detail=f"Category '{category.name}' already exists (found '{existing_name.name}')",
            )

    updated_category = category_service.update_category(
        db=db, category_id=category_id, category=category
    )
    if not updated_category:
        raise HTTPException(status_code=404, detail="Category not found")

    return updated_category


@router.delete("/{category_id}", response_model=CategoryDelete)
def delete_category(category_id: int, db: Annotated[Session, Depends(get_db)]) -> dict[str, Any]:
    """Delete a category by ID."""
    deleted = category_service.delete_category(db, category_id=category_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"id": category_id, "deleted": True}
