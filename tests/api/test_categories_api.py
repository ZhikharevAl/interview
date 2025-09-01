import allure

from tests.api.clients.categories import CategoriesClient


@allure.feature("Categories API")
class TestCategoriesAPI:
    """Tests for API categories using control fixtures."""

    @allure.story("Get Category by ID")
    def test_read_category_by_id(
        self, categories_client: CategoriesClient, managed_category: int
    ) -> None:
        """
        Test for successful retrieval of a category by ID.

        The `managed_category` fixture provides the ID of an already created category.
        """
        category_id = managed_category
        with allure.step(f"Requesting category by ID: {category_id}"):
            response = categories_client.get_by_id(category_id)

        with allure.step("Checking that the response data is correct"):
            assert response.ok
            data = response.json()
            assert data["id"] == category_id
            assert "name" in data
