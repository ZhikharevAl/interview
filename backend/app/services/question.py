from app.db.models.question import Question as QuestionModel
from app.schemas.question import QuestionCreate, QuestionUpdate
from sqlalchemy import func
from sqlalchemy.orm import Session


def get_all_questions(db: Session) -> list[QuestionModel]:
    """Get all questions."""
    return db.query(QuestionModel).all()


def get_question(db: Session, question_id: int) -> QuestionModel | None:
    """Get question by ID."""
    return db.query(QuestionModel).filter(QuestionModel.id == question_id).first()


def get_question_by_text_case_insensitive(db: Session, question_text: str) -> QuestionModel | None:
    """Get question by text (case insensitive)."""
    return (
        db.query(QuestionModel)
        .filter(func.lower(QuestionModel.question_text) == func.lower(question_text))
        .first()
    )


def get_questions_by_category(db: Session, category_id: int) -> list[QuestionModel]:
    """Get questions by category."""
    return db.query(QuestionModel).filter(QuestionModel.category_id == category_id).all()


def create_question(db: Session, question: QuestionCreate) -> QuestionModel:
    """Create a new question."""
    db_question = QuestionModel(**question.model_dump())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


def update_question(
    db: Session, question_id: int, question: QuestionUpdate
) -> QuestionModel | None:
    """Updates the question using only the passed fields."""
    db_question = db.get(QuestionModel, question_id)
    if not db_question:
        return None

    update_data = question.model_dump(exclude_unset=True)

    if update_data:
        for key, value in update_data.items():
            setattr(db_question, key, value)

        db.commit()
        db.refresh(db_question)

    return db_question


def delete_question(db: Session, question_id: int) -> QuestionModel | None:
    """Delete a question by ID."""
    db_question = db.query(QuestionModel).filter(QuestionModel.id == question_id).first()
    if db_question:
        db.delete(db_question)
        db.commit()
    return db_question
