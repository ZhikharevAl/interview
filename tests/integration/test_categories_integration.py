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
