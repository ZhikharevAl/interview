from typing import Annotated, Any

from app.db.database import get_db
from app.schemas.question import Question, QuestionCreate, QuestionDelete, QuestionUpdate
from app.services import question as question_service
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/")
def read_questions(
    db: Annotated[Session, Depends(get_db)], category_id: int | None = None
) -> list[Question]:
    """Get questions by category ID."""
    if category_id:
        questions = question_service.get_questions_by_category(db=db, category_id=category_id)
        if not questions:
            return []
        return [Question.model_validate(q) for q in questions]

    all_questions = question_service.get_all_questions(db=db)
    return [Question.model_validate(q) for q in all_questions]


@router.get("/{question_id}")
def read_question(question_id: int, db: Annotated[Session, Depends(get_db)]) -> Question:
    """Get question by ID."""
    db_question = question_service.get_question(db, question_id=question_id)
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return Question.model_validate(db_question)


@router.post("/")
def create_question(question: QuestionCreate, db: Annotated[Session, Depends(get_db)]) -> Question:
    """Create a new question."""
    db_question = question_service.create_question(db=db, question=question)
    return Question.model_validate(db_question)


@router.put("/{question_id}", response_model=Question)
def update_question(
    question_id: int, question: QuestionUpdate, db: Annotated[Session, Depends(get_db)]
) -> question_service.QuestionModel:
    """Update a question by ID."""
    updated_question = question_service.update_question(
        db=db, question_id=question_id, question=question
    )
    if not updated_question:
        raise HTTPException(status_code=404, detail="Question not found")
    return updated_question


@router.delete("/{question_id}", response_model=QuestionDelete)
def delete_question(question_id: int, db: Annotated[Session, Depends(get_db)]) -> dict[str, Any]:
    """Delete a question by ID."""
    deleted = question_service.delete_question(db, question_id=question_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Question not found")
    return {"id": question_id, "deleted": True}
