from http import HTTPStatus

import allure
from fastapi.testclient import TestClient


@allure.feature("Categories Integration")
class TestCategoriesIntegration:
    """Integration tests for endpoint categories."""

    @allure.story("Create Category")
    @allure.title("Test successful category creation")
    def test_create_category_success(self, client: TestClient) -> None:
        """The test of successful category creation."""
        category_data = {"name": "Python"}

        with allure.step("Send request to create a new category"):
            response = client.post("/api/v1/categories/", json=category_data)

        with allure.step("Verify the response for successful creation"):
            assert response.status_code == HTTPStatus.CREATED, (
                "Expected status 201 CREATED on category creation."
            )
            data = response.json()
            assert data["name"] == "Python", (
                "The created category name does not match the sent name."
            )
            assert "id" in data, "The response from the server is missing the 'id' key."
            assert isinstance(data["id"], int), "The category ID must be an integer."

    @allure.story("Create Category")
    @allure.title("Test failure when creating a duplicate category")
    def test_create_duplicate_category_fails(self, client: TestClient) -> None:
        """A test that verifies the impossibility of creating a duplicate category."""
        category_data = {"name": "Duplicate Category"}

        with allure.step("Create an initial category"):
            response1 = client.post("/api/v1/categories/", json=category_data)
            assert response1.status_code == HTTPStatus.CREATED, (
                "Failed to create the initial category for the duplicate test."
            )

        with allure.step("Attempt to create a category with the same name"):
            response2 = client.post("/api/v1/categories/", json=category_data)

        with allure.step("Verify the response indicates a conflict"):
            assert response2.status_code == HTTPStatus.BAD_REQUEST, (
                "Expected status 400 BAD_REQUEST when creating a duplicate."
            )
            assert "already exists" in response2.json()["detail"], (
                "The error message did not contain the expected 'already exists' text."
            )

    @allure.story("Get Category")
    @allure.title("Test getting a non-existent category")
    def test_get_nonexistent_category(self, client: TestClient) -> None:
        """The test for getting a non-existent category should return a 404."""
        with allure.step("Request a category with a non-existent ID"):
            response = client.get("/api/v1/categories/99999")

        with allure.step("Verify that the server returns a 404 Not Found error"):
            assert response.status_code == HTTPStatus.NOT_FOUND, (
                "Expected status 404 NOT_FOUND for a non-existent category."
            )
            assert "Category not found" in response.json()["detail"], (
                "The error message did not contain the expected 'Category not found' text."
            )

    @allure.story("Update Category")
    @allure.title("Test successful category update")
    def test_update_category(self, client: TestClient, sample_category: dict) -> None:
        """A test of a successful category update."""
        category_id = sample_category["id"]
        update_data = {"name": "Updated Category Name"}

        with allure.step(f"Send request to update category with ID {category_id}"):
            response = client.put(f"/api/v1/categories/{category_id}", json=update_data)

        with allure.step("Verify the category was updated successfully"):
            assert response.status_code == HTTPStatus.OK, (
                "Expected status 200 OK on category update."
            )
            data = response.json()
            assert data["id"] == category_id, (
                "The category ID in the response does not match the updated ID."
            )
            assert data["name"] == "Updated Category Name", "The category name was not updated."

    @allure.story("Get Category")
    @allure.title("Test getting a category by its ID")
    def test_get_category_by_id(self, client: TestClient, sample_category: dict) -> None:
        """The test of getting a category by ID."""
        category_id = sample_category["id"]

        with allure.step(f"Request category by ID {category_id}"):
            response = client.get(f"/api/v1/categories/{category_id}")

        with allure.step("Verify the response contains the correct category data"):
            assert response.status_code == HTTPStatus.OK, (
                "Expected status 200 OK when requesting a category by ID."
            )
            data = response.json()
            assert data["id"] == category_id, (
                "The returned category ID does not match the requested ID."
            )
            assert data["name"] == sample_category["name"], (
                "The returned category name does not match the expected name."
            )

    @allure.story("Update Category")
    @allure.title("Test updating a non-existent category")
    def test_update_nonexistent_category(self, client: TestClient) -> None:
        """An update test for a non-existent category should return a 404."""
        update_data = {"name": "Non-existent"}

        with allure.step("Send request to update a non-existent category"):
            response = client.put("/api/v1/categories/99999", json=update_data)

        with allure.step("Verify that the server returns a 404 Not Found error"):
            assert response.status_code == HTTPStatus.NOT_FOUND, (
                "Expected status 404 NOT_FOUND when updating a non-existent category."
            )
            assert "Category not found" in response.json()["detail"], (
                "The error message did not contain 'Category not found'."
            )

    @allure.story("Delete Category")
    @allure.title("Test successful category deletion")
    def test_delete_category(self, client: TestClient, sample_category: dict) -> None:
        """A test for successfully deleting a category."""
        category_id = sample_category["id"]

        with allure.step(f"Send request to delete category with ID {category_id}"):
            response = client.delete(f"/api/v1/categories/{category_id}")

        with allure.step("Verify the deletion was successful"):
            assert response.status_code == HTTPStatus.OK, (
                "Expected status 200 OK on category deletion."
            )
            data = response.json()
            assert data["deleted"] is True, "The 'deleted' flag in the response should be True."
            assert data["id"] == category_id, (
                "The response ID does not match the deleted category's ID."
            )

        with allure.step("Verify the category is no longer accessible"):
            get_response = client.get(f"/api/v1/categories/{category_id}")
            assert get_response.status_code == HTTPStatus.NOT_FOUND, (
                "The category was still accessible after deletion."
            )

    @allure.story("Delete Category")
    @allure.title("Test deleting a non-existent category")
    def test_delete_nonexistent_category(self, client: TestClient) -> None:
        """The deletion test for a non-existent category should return a 404."""
        with allure.step("Send request to delete a non-existent category"):
            response = client.delete("/api/v1/categories/99999")

        with allure.step("Verify that the server returns a 404 Not Found error"):
            assert response.status_code == HTTPStatus.NOT_FOUND, (
                "Expected status 404 NOT_FOUND when deleting a non-existent category."
            )
            assert "Category not found" in response.json()["detail"], (
                "The error message did not contain 'Category not found'."
            )

    @allure.story("Delete Category")
    @allure.title("Test cascade deletion of questions when a category is deleted")
    def test_category_cascade_delete_questions(
        self, client: TestClient, sample_category: dict
    ) -> None:
        """A cascade deletion test for questions when deleting a category."""
        category_id = sample_category["id"]

        with allure.step("Create a question associated with the category"):
            question_data = {
                "question_text": "Test question?",
                "answer_text": "Test answer.",
                "category_id": category_id,
            }
            question_response = client.post("/api/v1/questions/", json=question_data)
            assert question_response.status_code == HTTPStatus.CREATED, (
                "Failed to create a question for the test."
            )
            question_id = question_response.json()["id"]

        with allure.step(f"Delete the category with ID {category_id}"):
            delete_response = client.delete(f"/api/v1/categories/{category_id}")
            assert delete_response.status_code == HTTPStatus.OK, (
                "Failed to delete the category to test cascade deletion."
            )

        with allure.step("Verify that the associated question was also deleted"):
            question_get_response = client.get(f"/api/v1/questions/{question_id}")
            assert question_get_response.status_code == HTTPStatus.NOT_FOUND, (
                "The question was not deleted as part of the cascade delete."
            )
