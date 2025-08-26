from pydantic import BaseModel


class CategoryBase(BaseModel):
    """Category base schema."""

    name: str


class CategoryCreate(CategoryBase):
    """Category creation schema."""


class Category(CategoryBase):
    """Category schema."""

    id: int
