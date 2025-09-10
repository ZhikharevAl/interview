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
            assert response.ok, (
                f"Health endpoint returned a non-OK status code: {response.status_text}"
            )
            data = response.json()
            assert data["status"] == "healthy", (
                f"Expected status to be 'healthy', but got '{data.get('status')}'"
            )
            assert "version" in data, "The 'version' key is missing from the health check response"
            assert "database_url" in data, (
                "The 'database_url' key is missing from the health check response"
            )

    @allure.story("Root Endpoint")
    def test_root_endpoint(self, api_client: HTTPClient) -> None:
        """Test that root endpoint is accessible."""
        with allure.step("Requesting root endpoint"):
            response = api_client.get("/")

        with allure.step("Verifying root endpoint response"):
            assert response.ok, (
                f"Root endpoint returned a non-OK status code: {response.status_text}"
            )
