from playwright.sync_api import APIResponse

from tests.api.clients.base_api import BaseAPI


class CategoriesClient(BaseAPI):
    """API client for interacting with category endpoints (/api/v1/categories)."""

    BASE_URL = "/api/v1/categories"

    def create(self, name: str) -> APIResponse:
        """Sends a request to create a new category."""
        payload = {"name": name}
        return self.http.post(self.BASE_URL, json=payload)

    def get_all(self) -> APIResponse:
        """Sends a request to retrieve all categories."""
        return self.http.get(self.BASE_URL)

    def get_by_id(self, category_id: int) -> APIResponse:
        """Sends a request to retrieve a category by its ID."""
        return self.http.get(f"{self.BASE_URL}/{category_id}")

    def delete(self, category_id: int) -> APIResponse:
        """Sends a request to delete a category by its ID."""
        return self.http.delete(f"{self.BASE_URL}/{category_id}")
