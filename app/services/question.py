from sqlalchemy.orm import Session

from app.db.models.question import Question as QuestionModel
from app.schemas.question import QuestionCreate


def get_all_questions(db: Session) -> list[QuestionModel]:
    """Get all questions."""
    return db.query(QuestionModel).all()


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
