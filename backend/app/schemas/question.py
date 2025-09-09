from pydantic import BaseModel, ConfigDict


class QuestionBase(BaseModel):
    """Question base schema."""

    question_text: str
    answer_text: str
    category_id: int | None = None


class QuestionCreate(QuestionBase):
    """Question creation schema."""

    model_config = ConfigDict(from_attributes=True)


class QuestionUpdate(BaseModel):
    """Question update schema."""

    question_text: str | None = None
    answer_text: str | None = None
    category_id: int | None = None

    model_config = ConfigDict(from_attributes=True)


class Question(QuestionBase):
    """Question schema."""

    id: int

    model_config = ConfigDict(from_attributes=True)


class QuestionDelete(BaseModel):
    """Schema for delete confirmation."""

    id: int
    deleted: bool

    model_config = ConfigDict(from_attributes=True)
