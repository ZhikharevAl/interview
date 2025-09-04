from http import HTTPStatus

import allure

from tests.api.clients.categories import CategoriesClient
from tests.utils.category_model import CategoryData


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

    @allure.story("Delete Category")
    def test_delete_category(self, categories_client: CategoriesClient) -> None:
        """A test for the successful deletion of a category."""
        category_name = "Category to be deleted"
        with allure.step(f"Creating category '{category_name}' for deletion"):
            create_response = categories_client.create(name=category_name)
            assert create_response.ok
            category_id = create_response.json()["id"]

        with allure.step(f"Deleting category by ID: {category_id}"):
            delete_response = categories_client.delete(category_id)

        with allure.step("We check that the deletion was successful."):
            assert delete_response.ok
            assert delete_response.json()["deleted"] is True

        with allure.step(
            "We check that the category has indeed been deleted (we are waiting for 404)"
        ):
            get_response = categories_client.get_by_id(category_id)
            assert get_response.status == HTTPStatus.NOT_FOUND

    @allure.story("Get Category by ID")
    def test_read_nonexistent_category(self, categories_client: CategoriesClient) -> None:
        """Test for getting 404 errors when requesting a non-existent category."""
        non_existent_id = CategoryData.random_number()
        with allure.step(f"Requesting a non-existent software category ID: {non_existent_id}"):
            response = categories_client.get_by_id(non_existent_id)

        with allure.step("Checking that the API returned a 404 Not Found error"):
            assert response.status == HTTPStatus.NOT_FOUND
