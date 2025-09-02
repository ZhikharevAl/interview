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


class CategoryUpdate(BaseModel):
    """Category update schema."""

    name: str | None = None


class CategoryDelete(BaseModel):
    """Schema for delete confirmation."""

    id: int
    deleted: bool
