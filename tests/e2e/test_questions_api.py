import allure

from tests.api.clients.questions import QuestionsClient
from tests.utils.question_model import QuestionData


class TestQuestionsAPI:
    """Tests for API questions (/api/v1/questions)."""

    @allure.story("Create Question")
    def test_create_question(
        self, questions_client: QuestionsClient, managed_category: int
    ) -> None:
        """Test for the successful creation of a question."""
        question_data = QuestionData.random()

        with allure.step("Sending a request to create a new question"):
            response = questions_client.create(
                category_id=managed_category,
                question_text=question_data.question_text,
                answer_text=question_data.answer_text,
            )

        with allure.step("Checking the successful creation of a question"):
            assert response.ok, (
                f"Failed to create question. Status: {response.status}, Body: {response.text()}"
            )

            response_json = response.json()

            assert "id" in response_json, (
                "The 'id' key is missing from the question creation response."
            )
            assert response_json["question_text"] == question_data.question_text, (
                "The 'question_text' in the response does not match the sent data."
            )
            assert response_json["answer_text"] == question_data.answer_text, (
                "The 'answer_text' in the response does not match the sent data."
            )
            assert response_json["category_id"] == managed_category, (
                "The 'category_id' in the response does not match the provided category ID."
            )

    @allure.story("Get Question by ID")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_read_question_by_id(
        self, questions_client: QuestionsClient, managed_question: int
    ) -> None:
        """Test for successful retrieval of a question by ID."""
        question_id = managed_question

        with allure.step(f"Requesting question by ID: {question_id}"):
            response = questions_client.get_by_id(question_id)

        with allure.step("Verifying response data"):
            assert response.ok, f"Failed to get question by ID. Status: {response.status}"
            data = response.json()
            assert data["id"] == question_id, (
                f"Expected question ID {question_id}, but got {data.get('id')}"
            )
            assert "question_text" in data, "The 'question_text' key is missing"
            assert "answer_text" in data, "The 'answer_text' key is missing"
            assert "category_id" in data, "The 'category_id' key is missing"
