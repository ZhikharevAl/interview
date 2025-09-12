from app.db.models.category import Category as CategoryModel
from app.schemas.category import CategoryCreate, CategoryUpdate
from sqlalchemy import func
from sqlalchemy.orm import Session


def get_categories(db: Session, skip: int = 0, limit: int = 100) -> list[CategoryModel]:
    """Get categories."""
    return db.query(CategoryModel).offset(skip).limit(limit).all()


def get_category(db: Session, category_id: int) -> CategoryModel | None:
    """Get category by ID."""
    return db.query(CategoryModel).filter(CategoryModel.id == category_id).first()


def get_category_by_name(db: Session, name: str) -> CategoryModel | None:
    """Get category by name."""
    return (
        db.query(CategoryModel).filter(func.lower(CategoryModel.name) == func.lower(name)).first()
    )


def create_category(db: Session, category: CategoryCreate) -> CategoryModel:
    """Create a new category."""
    db_category = CategoryModel(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def update_category(
    db: Session, category_id: int, category: CategoryUpdate
) -> CategoryModel | None:
    """Partially updates the category by ID, changing only the passed fields."""
    db_category = db.get(CategoryModel, category_id)
    if not db_category:
        return None

    update_data = category.model_dump(exclude_unset=True)

    if update_data:
        for key, value in update_data.items():
            setattr(db_category, key, value)

        db.commit()
        db.refresh(db_category)

    return db_category


def delete_category(db: Session, category_id: int) -> CategoryModel | None:
    """Delete a category by ID."""
    db_category = db.query(CategoryModel).filter(CategoryModel.id == category_id).first()
    if db_category:
        db.delete(db_category)
        db.commit()
    return db_category
