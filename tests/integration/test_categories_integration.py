from http import HTTPStatus

from fastapi.testclient import TestClient


class TestCategoriesIntegration:
    """Integration tests for endpoint categories."""

    def test_create_category_success(self, client: TestClient) -> None:
        """The test of successful category creation."""
        category_data = {"name": "Python"}

        response = client.post("/api/v1/categories/", json=category_data)

        assert response.status_code == HTTPStatus.CREATED, (
            "The 201 CREATED status was expected when creating the category."
        )
        data = response.json()
        assert data["name"] == "Python", (
            "The name of the created category does not match the submitted one"
        )
        assert "id" in data, "The server's response is missing the 'id' key"
        assert isinstance(data["id"], int), "The type of the category ID must be an integer"

    def test_create_duplicate_category_fails(self, client: TestClient) -> None:
        """A test that verifies the impossibility of creating a duplicate category."""
        category_data = {"name": "Duplicate Category"}

        response1 = client.post("/api/v1/categories/", json=category_data)
        assert response1.status_code == HTTPStatus.CREATED, (
            "Couldn't create a source category for the test"
        )

        response2 = client.post("/api/v1/categories/", json=category_data)
        assert response2.status_code == HTTPStatus.BAD_REQUEST, (
            "The 400 BAD_REQUEST status was expected when creating a duplicate."
        )
        assert "already exists" in response2.json()["detail"], (
            "The text about the existing category was not found in the error message."
        )

    def test_get_nonexistent_category(self, client: TestClient) -> None:
        """The test for getting a non-existent category should return a 404."""
        response = client.get("/api/v1/categories/99999")

        assert response.status_code == HTTPStatus.NOT_FOUND, (
            "The 404 NOT_FOUND status was expected for a non-existent category"
        )
        assert "Category not found" in response.json()["detail"], (
            "The text 'Category not found' was not found in the error message"
        )

    def test_update_category(self, client: TestClient, sample_category: dict) -> None:
        """A test of a successful category update."""
        category_id = sample_category["id"]
        update_data = {"name": "Updated Category Name"}

        response = client.put(f"/api/v1/categories/{category_id}", json=update_data)

        assert response.status_code == HTTPStatus.OK, (
            "The 200 OK status was expected when updating the category"
        )
        data = response.json()
        assert data["id"] == category_id, (
            "The category ID in the response does not match the ID of the category being updated"
        )
        assert data["name"] == "Updated Category Name", "The category name has not been updated"

    def test_get_category_by_id(self, client: TestClient, sample_category: dict) -> None:
        """The test of getting a category by ID."""
        category_id = sample_category["id"]

        response = client.get(f"/api/v1/categories/{category_id}")

        assert response.status_code == HTTPStatus.OK, (
            "The 200 OK status was expected when requesting a category by ID."
        )
        data = response.json()
        assert data["id"] == category_id, (
            "The ID of the received category does not match the requested one"
        )
        assert data["name"] == sample_category["name"], (
            "The name of the received category does not match the expected one"
        )

    def test_update_nonexistent_category(self, client: TestClient) -> None:
        """An update test for a non-existent category should return a 404."""
        update_data = {"name": "Non-existent"}

        response = client.put("/api/v1/categories/99999", json=update_data)

        assert response.status_code == HTTPStatus.NOT_FOUND, (
            "The 404 NOT_FOUND status was expected when updating a non-existent category."
        )
        assert "Category not found" in response.json()["detail"], (
            "The text 'Category not found' was not found in the error message"
        )

    def test_delete_category(self, client: TestClient, sample_category: dict) -> None:
        """A test for successfully deleting a category."""
        category_id = sample_category["id"]

        response = client.delete(f"/api/v1/categories/{category_id}")

        assert response.status_code == HTTPStatus.OK, (
            "The 200 OK status was expected when deleting a category."
        )
        data = response.json()

        assert data["deleted"] is True, "The 'deleted' flag in the response must be True."
        assert data["id"] == category_id, (
            "The ID in the response does not match the ID of the deleted category"
        )

        get_response = client.get(f"/api/v1/categories/{category_id}")
        assert get_response.status_code == HTTPStatus.NOT_FOUND, (
            "The category is still available after deletion."
        )

    def test_delete_nonexistent_category(self, client: TestClient) -> None:
        """The deletion test for a non-existent category should return a 404."""
        response = client.delete("/api/v1/categories/99999")

        assert response.status_code == HTTPStatus.NOT_FOUND, (
            "The 404 NOT_FOUND status was expected when deleting a non-existent category."
        )
        assert "Category not found" in response.json()["detail"], (
            "The text 'Category not found' was not found in the error message"
        )

    def test_category_cascade_delete_questions(
        self, client: TestClient, sample_category: dict
    ) -> None:
        """A cascade deletion test for questions when deleting a category."""
        category_id = sample_category["id"]

        question_data = {
            "question_text": "Test question?",
            "answer_text": "Test answer.",
            "category_id": category_id,
        }
        question_response = client.post("/api/v1/questions/", json=question_data)
        assert question_response.status_code == HTTPStatus.CREATED, (
            "Couldn't create a question for the test"
        )
        question_id = question_response.json()["id"]

        delete_response = client.delete(f"/api/v1/categories/{category_id}")
        assert delete_response.status_code == HTTPStatus.OK, (
            "Couldn't delete category to check for cascading deletion"
        )

        question_get_response = client.get(f"/api/v1/questions/{question_id}")
        assert question_get_response.status_code == HTTPStatus.NOT_FOUND, (
            "The question was not deleted cascadingly along with the category"
        )
