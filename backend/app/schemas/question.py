from pydantic import BaseModel, ConfigDict


class QuestionBase(BaseModel):
    """Question base schema."""

    question_text: str
    answer_text: str
    category_id: int


class QuestionCreate(QuestionBase):
    """Question creation schema."""


class Question(QuestionBase):
    """Question schema."""

    id: int

    model_config = ConfigDict(from_attributes=True)
