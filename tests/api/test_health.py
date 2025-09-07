import allure

from tests.utils.http_client import HTTPClient


@allure.feature("Health Check")
class TestHealthCheck:
    """Tests for application health endpoints."""

    @allure.story("Health Check")
    def test_health_endpoint(self, api_client: HTTPClient) -> None:
        """Test that health endpoint returns correct status."""
        with allure.step("Requesting health endpoint"):
            response = api_client.get("/health")

        with allure.step("Verifying health response"):
            assert response.ok
            data = response.json()
            assert data["status"] == "healthy"
            assert "version" in data
            assert "database_url" in data
