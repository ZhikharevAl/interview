from playwright.sync_api import APIResponse

from tests.api.clients.base_api import BaseAPI
from tests.config.config import ConfigTests


class QuestionsClient(BaseAPI):
    """API client for interacting with question endpoints (/api/v1/questions)."""

    def create(self, category_id: int, question_text: str, answer_text: str) -> APIResponse:
        """Sends a request to create a new question."""
        payload = {
            "category_id": category_id,
            "question_text": question_text,
            "answer_text": answer_text,
        }
        return self.http.post(ConfigTests.QUESTIONS_URL, json=payload)

    def get_all(self, category_id: int | None = None) -> APIResponse:
        """Sends a request to retrieve all questions or questions by category."""
        params = {"category_id": category_id} if category_id else None
        return self.http.get(ConfigTests.QUESTIONS_URL, params=params)

    def get_by_id(self, question_id: int) -> APIResponse:
        """Sends a request to retrieve a question by its ID."""
        return self.http.get(f"{ConfigTests.QUESTIONS_URL}/{question_id}")

    def update(
        self,
        question_id: int,
        category_id: int | None = None,
        question_text: str | None = None,
        answer_text: str | None = None,
    ) -> APIResponse:
        """Sends a request to update a question."""
        payload = {}
        if category_id is not None:
            payload["category_id"] = category_id
        if question_text is not None:
            payload["question_text"] = question_text
        if answer_text is not None:
            payload["answer_text"] = answer_text

        return self.http.put(f"{ConfigTests.QUESTIONS_URL}/{question_id}", json=payload)

    def delete(self, question_id: int) -> APIResponse:
        """Sends a request to delete a question by its ID."""
        return self.http.delete(f"{ConfigTests.QUESTIONS_URL}/{question_id}")
