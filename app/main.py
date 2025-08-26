from fastapi import FastAPI

from app.schemas.category import Category, CategoryCreate
from app.schemas.question import Question

app = FastAPI(title="Interview Prep App")

categories_db = [
    {"id": 1, "name": "Python"},
    {"id": 2, "name": "JavaScript"},
    {"id": 3, "name": "Алгоритмы"},
]

questions_db = [
    {
        "id": 1,
        "question_text": "Что такое список в Python?",
        "answer_text": "Список - это изменяемая структура данных...",
        "category_id": 1,
    },
    {
        "id": 2,
        "question_text": "Что такое замыкание в JavaScript?",
        "answer_text": "Замыкание - это функция, которая имеет доступ...",
        "category_id": 2,
    },
]


@app.get("/")
def read_root() -> dict[str, str]:
    """Welcome message."""
    return {"message": "Welcome to Interview Prep App!"}


@app.get("/categories", response_model=list[Category])
def get_categories() -> list[dict[str, int]]:
    """Get all categories."""
    return categories_db


@app.get("/questions", response_model=list[Question])
def get_questions(category_id: int | None) -> list[dict[str, int]]:
    """Get questions for a specific category."""
    if category_id:
        return [q for q in questions_db if q["category_id"] == category_id]
    return questions_db


@app.post("/categories", response_model=Category)
def create_category(category: CategoryCreate) -> dict[str, int]:
    """Create a new category."""
    new_id = max([c["id"] for c in categories_db]) + 1
    new_category = {"id": new_id, "name": category.name}
    categories_db.append(new_category)
    return new_category
