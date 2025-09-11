from playwright.sync_api import APIResponse

from tests.api.clients.base_api import BaseAPI
from tests.config.config import ConfigTests


class CategoriesClient(BaseAPI):
    """API client for interacting with category endpoints."""

    def create(self, name: str) -> APIResponse:
        """Sends a request to create a new category."""
        payload = {"name": name}
        return self.http.post(ConfigTests.CATEGORIES_ENDPOINT, json=payload)

    def get_all(self) -> APIResponse:
        """Sends a request to retrieve all categories."""
        return self.http.get(ConfigTests.CATEGORIES_ENDPOINT)

    def get_by_id(self, category_id: int) -> APIResponse:
        """Sends a request to retrieve a category by its ID."""
        path = f"{ConfigTests.CATEGORIES_ENDPOINT}/{category_id}"
        return self.http.get(path)

    def delete(self, category_id: int) -> APIResponse:
        """Sends a request to delete a category by its ID."""
        path = f"{ConfigTests.CATEGORIES_ENDPOINT}/{category_id}"
        return self.http.delete(path)
