from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.question import Question, QuestionCreate
from app.services import question as question_service

router = APIRouter()


@router.get("/")
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


@router.post("/", response_model=Question)
def create_question(
    question: QuestionCreate, db: Annotated[Session, Depends(get_db)]
) -> question_service.QuestionModel:
    """Create a new question."""
    return question_service.create_question(db=db, question=question)
