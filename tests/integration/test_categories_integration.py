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
