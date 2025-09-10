from collections.abc import Generator

import pytest
from playwright.sync_api import APIRequestContext, Playwright

from tests.api.clients.categories import CategoriesClient
from tests.api.clients.questions import QuestionsClient
from tests.config.config import ConfigTests
from tests.utils.category_model import CategoryData
from tests.utils.http_client import HTTPClient
from tests.utils.question_model import QuestionData


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
def questions_client(api_client: HTTPClient) -> QuestionsClient:
    """Provides a high-level client for the Questions API."""
    return QuestionsClient(api_client)


@pytest.fixture
def managed_category(categories_client: CategoriesClient) -> Generator[int]:
    """
    Control fixture: Creates a category before the test and deletes it after.

    `yields` ID the created category.
    """
    category = CategoryData.random()
    response = categories_client.create(name=category.name)
    category_id = response.json()["id"]

    yield category_id

    delete_response = categories_client.delete(category_id)
    assert delete_response.ok, f"Failed to delete category {category_id} in test teardown"


@pytest.fixture
def managed_question(questions_client: QuestionsClient, managed_category: int) -> Generator[int]:
    """
    Control fixture: Creates a question before the test and deletes it after.

    Yields ID of the created question.
    """
    question = QuestionData.random()
    response = questions_client.create(
        category_id=managed_category,
        question_text=question.question_text,
        answer_text=question.answer_text,
    )
    assert response.ok, f"Failed to create question: {response.text()}"
    question_id = response.json()["id"]

    yield question_id

    delete_response = questions_client.delete(question_id)
    assert delete_response.ok, f"Failed to delete question {question_id} in test teardown"
