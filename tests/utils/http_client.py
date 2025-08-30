import logging
from typing import Any

from playwright.sync_api import APIRequestContext, APIResponse

from tests.utils.allure_utils import AllureUtils

TIMEOUT = 30000


class HTTPClient:
    """Low-level HTTP client using Playwright's APIRequestContext."""

    def __init__(self, api_context: APIRequestContext) -> None:
        """Initializes HTTPClient."""
        self.api_request_context: APIRequestContext = api_context
        self.logger = logging.getLogger(__name__)

    def get(
        self,
        endpoint: str,
        headers: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> APIResponse:
        """Sends a GET request."""
        self.logger.info("Sending GET to %s with params: %s", endpoint, params)
        response: APIResponse = self.api_request_context.get(
            endpoint, headers=headers, params=params, timeout=TIMEOUT
        )
        self.logger.info("Received response %s from %s", response.status, response.url)
        AllureUtils.attach_response(response)
        return response

    def post(
        self,
        endpoint: str,
        headers: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        json: Any | None = None,  # noqa: ANN401
    ) -> APIResponse:
        """Sends a POST request."""
        self.logger.info("Sending POST to %s", endpoint)
        response: APIResponse = self.api_request_context.post(
            endpoint,
            headers=headers,
            data=json,
            form=data,
            timeout=TIMEOUT,
        )
        self.logger.info("Received response %s from %s", response.status, response.url)
        AllureUtils.attach_response(response)
        return response

    def put(
        self,
        endpoint: str,
        headers: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        json: Any | None = None,  # noqa: ANN401
    ) -> APIResponse:
        """Sends a PUT request."""
        self.logger.info("Sending PUT to %s", endpoint)
        response: APIResponse = self.api_request_context.put(
            endpoint,
            headers=headers,
            data=json,
            form=data,
            timeout=TIMEOUT,
        )
        self.logger.info("Received response %s from %s", response.status, response.url)
        AllureUtils.attach_response(response)
        return response

    def delete(
        self,
        endpoint: str,
        headers: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> APIResponse:
        """Sends a DELETE request."""
        self.logger.info("Sending DELETE to %s", endpoint)
        response: APIResponse = self.api_request_context.delete(
            endpoint, headers=headers, params=params, timeout=TIMEOUT
        )
        self.logger.info("Received response %s from %s", response.status, response.url)
        AllureUtils.attach_response(response)
        return response

    def patch(
        self,
        endpoint: str,
        headers: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        json: Any | None = None,  # noqa: ANN401
    ) -> APIResponse:
        """Sends a PATCH request."""
        self.logger.info("Sending PATCH to %s", endpoint)
        response: APIResponse = self.api_request_context.patch(
            endpoint,
            headers=headers,
            data=json,
            form=data,
            timeout=TIMEOUT,
        )
        self.logger.info("Received response %s from %s", response.status, response.url)
        AllureUtils.attach_response(response)
        return response
