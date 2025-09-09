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
