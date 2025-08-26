from pydantic import BaseModel, ConfigDict


class CategoryBase(BaseModel):
    """Category base schema."""

    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class CategoryCreate(CategoryBase):
    """Category creation schema."""


class Category(CategoryBase):
    """Category schema."""

    id: int
