from http import HTTPStatus

import allure
from fastapi.testclient import TestClient


@allure.feature("Questions Integration")
class TestQuestionsIntegration:
    """Integration tests for questions endpoint."""

    @allure.story("Create Question")
    @allure.title("Test successful question creation")
    def test_create_question_success(self, client: TestClient, sample_category: dict) -> None:
        """Test successful question creation."""
        question_data = {
            "question_text": "What is FastAPI?",
            "answer_text": "FastAPI is a modern web framework for building APIs with Python.",
            "category_id": sample_category["id"],
        }

        with allure.step("Send request to create a new question"):
            response = client.post("/api/v1/questions/", json=question_data)

        with allure.step("Verify the response for successful creation"):
            assert response.status_code == HTTPStatus.CREATED, (
                "Expected status 201 CREATED on question creation."
            )
            data = response.json()
            assert data["question_text"] == question_data["question_text"], (
                "The question text does not match."
            )
            assert data["answer_text"] == question_data["answer_text"], (
                "The answer text does not match."
            )
            assert data["category_id"] == sample_category["id"], "The category ID does not match."
            assert "id" in data, "The response is missing the 'id' key."

    @allure.story("Create Question")
    @allure.title("Test failure when creating a duplicate question")
    def test_create_duplicate_question_fails(
        self, client: TestClient, sample_category: dict
    ) -> None:
        """Test that creating duplicate question fails."""
        question_data = {
            "question_text": "What is duplicate testing?",
            "answer_text": "Testing for duplicates.",
            "category_id": sample_category["id"],
        }
        with allure.step("Create an initial question"):
            response1 = client.post("/api/v1/questions/", json=question_data)
            assert response1.status_code == HTTPStatus.CREATED, (
                "Failed to create the initial question."
            )

        with allure.step("Attempt to create a duplicate question"):
            response2 = client.post("/api/v1/questions/", json=question_data)

        with allure.step("Verify the server returns a conflict error"):
            assert response2.status_code == HTTPStatus.BAD_REQUEST, (
                "Expected 400 BAD_REQUEST for duplicate."
            )
            assert "already exists" in response2.json()["detail"], (
                "Error message did not indicate a duplicate."
            )

    @allure.story("Get Questions")
    @allure.title("Test getting a list of all questions")
    def test_get_all_questions(self, client: TestClient, sample_category: dict) -> None:
        """Test getting all questions."""
        with allure.step("Create multiple questions"):
            questions = [
                {"question_text": "Q1?", "answer_text": "A1", "category_id": sample_category["id"]},
                {"question_text": "Q2?", "answer_text": "A2", "category_id": sample_category["id"]},
                {"question_text": "Q3?", "answer_text": "A3", "category_id": sample_category["id"]},
            ]
            for question in questions:
                client.post("/api/v1/questions/", json=question)

        with allure.step("Request the list of all questions"):
            response = client.get("/api/v1/questions/")

        with allure.step("Verify the response contains all created questions"):
            assert response.status_code == HTTPStatus.OK, (
                "Expected 200 OK when fetching all questions."
            )
            data = response.json()
            length_questions = 3
            assert len(data) >= length_questions, (
                "The number of returned questions is less than expected."
            )

    @allure.story("Get Questions")
    @allure.title("Test filtering questions by category ID")
    def test_get_questions_by_category(self, client: TestClient) -> None:
        """Test getting questions by category."""
        with allure.step("Create two distinct categories and associated questions"):
            cat1_response = client.post("/api/v1/categories/", json={"name": "Category 1"})
            cat2_response = client.post("/api/v1/categories/", json={"name": "Category 2"})
            cat1_id = cat1_response.json()["id"]
            cat2_id = cat2_response.json()["id"]
            client.post(
                "/api/v1/questions/",
                json={"question_text": "Q in Cat 1?", "answer_text": "A1", "category_id": cat1_id},
            )
            client.post(
                "/api/v1/questions/",
                json={"question_text": "Q in Cat 2?", "answer_text": "A2", "category_id": cat2_id},
            )

        with allure.step(f"Request questions filtered by category ID {cat1_id}"):
            response = client.get(f"/api/v1/questions/?category_id={cat1_id}")

        with allure.step("Verify the response contains only questions from the specified category"):
            assert response.status_code == HTTPStatus.OK, "Expected 200 OK for filtered questions."
            data = response.json()
            assert len(data) == 1, "Expected exactly one question in the filtered response."
            assert data[0]["category_id"] == cat1_id, (
                "The question's category ID does not match the filter."
            )

    @allure.story("Get Question")
    @allure.title("Test getting a single question by its ID")
    def test_get_question_by_id(self, client: TestClient, sample_question: dict) -> None:
        """Test getting question by ID."""
        question_id = sample_question["id"]
        with allure.step(f"Request question by ID {question_id}"):
            response = client.get(f"/api/v1/questions/{question_id}")

        with allure.step("Verify the response contains the correct question data"):
            assert response.status_code == HTTPStatus.OK, "Expected 200 OK when fetching by ID."
            data = response.json()
            assert data["id"] == question_id, "Returned question ID does not match."
            assert data["question_text"] == sample_question["question_text"], (
                "Returned question text does not match."
            )

    @allure.story("Get Question")
    @allure.title("Test getting a non-existent question")
    def test_get_nonexistent_question(self, client: TestClient) -> None:
        """Test getting non-existent question returns 404."""
        with allure.step("Request a question with a non-existent ID"):
            response = client.get("/api/v1/questions/99999")

        with allure.step("Verify the server returns a 404 Not Found error"):
            assert response.status_code == HTTPStatus.NOT_FOUND, (
                "Expected 404 NOT_FOUND for non-existent question."
            )
            assert "Question not found" in response.json()["detail"], (
                "Error message did not contain 'Question not found'."
            )

    @allure.story("Update Question")
    @allure.title("Test successful question update")
    def test_update_question(self, client: TestClient, sample_question: dict) -> None:
        """Test updating a question."""
        question_id = sample_question["id"]
        update_data = {"question_text": "Updated question?", "answer_text": "Updated answer."}

        with allure.step(f"Send request to update question with ID {question_id}"):
            response = client.put(f"/api/v1/questions/{question_id}", json=update_data)

        with allure.step("Verify the question was updated successfully"):
            assert response.status_code == HTTPStatus.OK, "Expected 200 OK on question update."
            data = response.json()
            assert data["id"] == question_id, "Question ID should not change on update."
            assert data["question_text"] == "Updated question?", "Question text was not updated."
            assert data["answer_text"] == "Updated answer.", "Answer text was not updated."

    @allure.story("Update Question")
    @allure.title("Test updating a question's category")
    def test_update_question_category(self, client: TestClient, sample_question: dict) -> None:
        """Test updating question's category."""
        with allure.step("Create a new category to assign to the question"):
            new_cat_response = client.post("/api/v1/categories/", json={"name": "New Category"})
            new_cat_id = new_cat_response.json()["id"]

        question_id = sample_question["id"]
        update_data = {"category_id": new_cat_id}
        with allure.step(f"Send request to update category for question ID {question_id}"):
            response = client.put(f"/api/v1/questions/{question_id}", json=update_data)

        with allure.step("Verify the question's category was updated"):
            assert response.status_code == HTTPStatus.OK, "Expected 200 OK when updating category."
            data = response.json()
            assert data["category_id"] == new_cat_id, "The question's category ID was not updated."

    @allure.story("Update Question")
    @allure.title("Test updating a non-existent question")
    def test_update_nonexistent_question(self, client: TestClient) -> None:
        """Test updating non-existent question returns 404."""
        with allure.step("Send request to update a non-existent question"):
            response = client.put("/api/v1/questions/99999", json={"question_text": "Non-existent"})

        with allure.step("Verify the server returns a 404 Not Found error"):
            assert response.status_code == HTTPStatus.NOT_FOUND, (
                "Expected 404 NOT_FOUND for non-existent question."
            )
            assert "Question not found" in response.json()["detail"], (
                "Error message did not contain 'Question not found'."
            )

    @allure.story("Delete Question")
    @allure.title("Test successful question deletion")
    def test_delete_question(self, client: TestClient, sample_question: dict) -> None:
        """Test deleting a question."""
        question_id = sample_question["id"]
        with allure.step(f"Send request to delete question with ID {question_id}"):
            response = client.delete(f"/api/v1/questions/{question_id}")

        with allure.step("Verify the deletion was successful"):
            assert response.status_code == HTTPStatus.OK, "Expected 200 OK on question deletion."
            data = response.json()
            assert data["deleted"] is True, "The 'deleted' flag should be True."
            assert data["id"] == question_id, "Response ID should match the deleted question's ID."

        with allure.step("Verify the question is no longer accessible"):
            get_response = client.get(f"/api/v1/questions/{question_id}")
            assert get_response.status_code == HTTPStatus.NOT_FOUND, (
                "The question was still accessible after deletion."
            )

    @allure.story("Delete Question")
    @allure.title("Test deleting a non-existent question")
    def test_delete_nonexistent_question(self, client: TestClient) -> None:
        """Test deleting non-existent question returns 404."""
        with allure.step("Send request to delete a non-existent question"):
            response = client.delete("/api/v1/questions/99999")

        with allure.step("Verify the server returns a 404 Not Found error"):
            assert response.status_code == HTTPStatus.NOT_FOUND, (
                "Expected 404 NOT_FOUND for non-existent question."
            )
            assert "Question not found" in response.json()["detail"], (
                "Error message did not contain 'Question not found'."
            )
