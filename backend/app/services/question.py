from app.db.models.question import Question as QuestionModel
from app.schemas.question import QuestionCreate, QuestionUpdate
from sqlalchemy.orm import Session


def get_all_questions(db: Session) -> list[QuestionModel]:
    """Get all questions."""
    return db.query(QuestionModel).all()


def get_question(db: Session, question_id: int) -> QuestionModel | None:
    """Get question by ID."""
    return db.query(QuestionModel).filter(QuestionModel.id == question_id).first()


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
    """Update a question by ID."""
    db_question = db.query(QuestionModel).filter(QuestionModel.id == question_id).first()
    if not db_question:
        return None

    if question.question_text is not None:
        db_question.question_text = question.question_text
    if question.answer_text is not None:
        db_question.answer_text = question.answer_text
    if question.category_id is not None:
        db_question.category_id = question.category_id

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
