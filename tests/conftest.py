from collections.abc import Generator

import pytest
from playwright.sync_api import APIRequestContext, Playwright

from tests.api.clients.categories import CategoriesClient
from tests.config.config import ConfigTests
from tests.utils.category_model import CategoryData
from tests.utils.http_client import HTTPClient


@pytest.fixture(scope="session", name="api_request_context")
def api_request_context_fixture(
    playwright: Playwright,
) -> Generator[APIRequestContext]:
    """Session-scoped fixture to create a Playwright APIRequestContext."""
    context = playwright.request.new_context(base_url=ConfigTests.APP_URL)
    yield context
    context.dispose()


@pytest.fixture
def api_client(api_request_context: APIRequestContext) -> HTTPClient:
    """Function-scoped fixture providing an instance of our custom HTTPClient."""
    return HTTPClient(api_request_context)


@pytest.fixture
def categories_client(api_client: HTTPClient) -> CategoriesClient:
    """Provides a high-level client for the Categories API."""
    return CategoriesClient(api_client)


@pytest.fixture
def managed_category(categories_client: CategoriesClient) -> Generator[int]:
    """
    Control fixture: Creates a category before the test and deletes it after.

    `yields` ID the created category.
    """
    category = CategoryData.random()
    response = categories_client.create(name=category.name, description=category.description)
    category_id = response.json()["id"]

    yield category_id

    delete_response = categories_client.delete(category_id)
    assert delete_response.ok, f"Failed to delete category {category_id} in test teardown"
