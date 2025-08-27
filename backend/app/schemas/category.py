from pydantic import BaseModel, ConfigDict


class CategoryBase(BaseModel):
    """Category base schema."""

    name: str


class CategoryCreate(CategoryBase):
    """Category creation schema."""


class Category(CategoryBase):
    """Category schema."""

    id: int

    model_config = ConfigDict(from_attributes=True)
