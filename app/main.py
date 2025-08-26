from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.database import Base, engine, get_db
from app.schemas.category import Category, CategoryCreate
from app.schemas.question import Question, QuestionCreate
from app.services import category as category_service
from app.services import question as question_service

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Interview Prep App", debug=settings.DEBUG)


@app.get("/")
def read_root() -> dict[str, str]:
    """Root endpoint."""
    return {"message": "Welcome to Interview Prep App!"}


@app.get("/categories")
def read_categories(
    db: Annotated[Session, Depends(get_db)], skip: int = 0, limit: int = 100
) -> list[Category]:
    """Get categories with pagination."""
    db_categories = category_service.get_categories(db, skip=skip, limit=limit)

    return [Category.model_config(db_cat) for db_cat in db_categories]  # pyright: ignore[reportCallIssue]


@app.post("/categories", response_model=Category)
def create_category(
    category: CategoryCreate, db: Annotated[Session, Depends(get_db)]
) -> category_service.CategoryModel:
    """Create a new category."""
    existing = category_service.get_category_by_name(db, category.name)
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")
    return category_service.create_category(db=db, category=category)


@app.get("/questions")
def read_questions(
    category_id: int | None, db: Annotated[Session, Depends(get_db)]
) -> list[Question]:
    """Get questions by category ID."""
    if category_id:
        questions = question_service.get_questions_by_category(db=db, category_id=category_id)
        if not questions:
            raise HTTPException(status_code=404, detail="Questions not found")
        return questions  # pyright: ignore[reportReturnType]
    return question_service.get_all_questions(db=db)  # pyright: ignore[reportReturnType]


@app.post("/questions", response_model=Question)
def create_question(
    question: QuestionCreate,
    db: Annotated[Session, Depends(get_db)],
) -> question_service.QuestionModel:
    """Create a new question."""
    return question_service.create_question(db=db, question=question)
