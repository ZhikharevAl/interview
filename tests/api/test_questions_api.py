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
            assert response.ok, f"Error creating question. Response: {response.text()}"

            response_json = response.json()

            assert "id" in response_json, "The response is missing the ID of the created question."
            assert response_json["question_text"] == question_data.question_text
            assert response_json["answer_text"] == question_data.answer_text
            assert response_json["category_id"] == managed_category
