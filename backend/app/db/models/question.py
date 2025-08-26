from app.db.database import Base
from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship


class Question(Base):
    """Question model."""

    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(Text, nullable=False)
    answer_text = Column(Text, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("Category", back_populates="questions")
