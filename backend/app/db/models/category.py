from typing import TYPE_CHECKING

from app.db.database import Base
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.db.models.question import Question


class Category(Base):
    """Category model."""

    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)

    questions: Mapped[list["Question"]] = relationship(
        "Question", back_populates="category", cascade="all, delete", passive_deletes=True
    )
