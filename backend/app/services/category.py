from app.db.models.category import Category as CategoryModel
from app.schemas.category import CategoryCreate, CategoryUpdate
from sqlalchemy.orm import Session


def get_categories(db: Session, skip: int = 0, limit: int = 100) -> list[CategoryModel]:
    """Get categories."""
    return db.query(CategoryModel).offset(skip).limit(limit).all()


def get_category(db: Session, category_id: int) -> CategoryModel | None:
    """Get category by ID."""
    return db.query(CategoryModel).filter(CategoryModel.id == category_id).first()


def get_category_by_name(db: Session, name: str) -> CategoryModel | None:
    """Get category by name."""
    return db.query(CategoryModel).filter(CategoryModel.name == name).first()


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
    """Update a category by ID."""
    db_category = db.query(CategoryModel).filter(CategoryModel.id == category_id).first()
    if not db_category:
        return None

    if category.name is not None:
        db_category.name = category.name

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
