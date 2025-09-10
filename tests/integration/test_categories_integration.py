from http import HTTPStatus

from fastapi.testclient import TestClient


class TestCategoriesIntegration:
    """Integration tests for categories endpoint."""

    def test_create_category_success(self, client: TestClient) -> None:
        """Test successful category creation."""
        category_data = {"name": "Python"}

        response = client.post("/api/v1/categories/", json=category_data)

        assert response.status_code == HTTPStatus.CREATED
        data = response.json()
        assert data["name"] == "Python"
        assert "id" in data
        assert isinstance(data["id"], int)

    def test_create_duplicate_category_fails(self, client: TestClient) -> None:
        """Test that creating duplicate category fails."""
        category_data = {"name": "Duplicate Category"}

        response1 = client.post("/api/v1/categories/", json=category_data)
        assert response1.status_code == HTTPStatus.CREATED

        response2 = client.post("/api/v1/categories/", json=category_data)
        assert response2.status_code == HTTPStatus.BAD_REQUEST
        assert "already exists" in response2.json()["detail"]

    def test_get_nonexistent_category(self, client: TestClient) -> None:
        """Test getting non-existent category returns 404."""
        response = client.get("/api/v1/categories/99999")

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert "Category not found" in response.json()["detail"]

    def test_update_category(self, client: TestClient, sample_category: dict) -> None:
        """Test updating a category."""
        category_id = sample_category["id"]
        update_data = {"name": "Updated Category Name"}

        response = client.put(f"/api/v1/categories/{category_id}", json=update_data)

        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert data["id"] == category_id
        assert data["name"] == "Updated Category Name"

    def test_get_category_by_id(self, client: TestClient, sample_category: dict) -> None:
        """Test getting category by ID."""
        category_id = sample_category["id"]

        response = client.get(f"/api/v1/categories/{category_id}")

        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert data["id"] == category_id
        assert data["name"] == sample_category["name"]

    def test_update_nonexistent_category(self, client: TestClient) -> None:
        """Test updating non-existent category returns 404."""
        update_data = {"name": "Non-existent"}

        response = client.put("/api/v1/categories/99999", json=update_data)

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert "Category not found" in response.json()["detail"]

    def test_delete_category(self, client: TestClient, sample_category: dict) -> None:
        """Test deleting a category."""
        category_id = sample_category["id"]

        response = client.delete(f"/api/v1/categories/{category_id}")

        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert data["deleted"] is True
        assert data["id"] == category_id

        get_response = client.get(f"/api/v1/categories/{category_id}")
        assert get_response.status_code == HTTPStatus.NOT_FOUND

    def test_delete_nonexistent_category(self, client: TestClient) -> None:
        """Test deleting non-existent category returns 404."""
        response = client.delete("/api/v1/categories/99999")

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert "Category not found" in response.json()["detail"]

    def test_category_cascade_delete_questions(
        self, client: TestClient, sample_category: dict
    ) -> None:
        """Test that deleting category cascades to delete questions."""
        category_id = sample_category["id"]

        question_data = {
            "question_text": "Test question?",
            "answer_text": "Test answer.",
            "category_id": category_id,
        }
        question_response = client.post("/api/v1/questions/", json=question_data)
        question_id = question_response.json()["id"]

        delete_response = client.delete(f"/api/v1/categories/{category_id}")
        assert delete_response.status_code == HTTPStatus.OK

        question_get_response = client.get(f"/api/v1/questions/{question_id}")
        assert question_get_response.status_code == HTTPStatus.NOT_FOUND
