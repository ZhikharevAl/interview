import json

import allure
from playwright.sync_api import APIResponse


class AllureUtils:
    """A collection of utility functions for Allure reporting."""

    @staticmethod
    def attach_response(response: APIResponse) -> None:
        """Attaches detailed HTTP response information to the Allure report."""
        try:
            body = response.json()
            body_text = json.dumps(body, indent=4, ensure_ascii=False)
        except json.JSONDecodeError:
            body_text = response.text()

        attachment_text = (
            f"URL: {response.url}\n"
            f"Status: {response.status} {response.status_text}\n\n"
            f"Headers:\n{json.dumps(dict(response.headers), indent=4)}\n\n"
            f"Body:\n{body_text}"
        )

        allure.attach(
            attachment_text,
            name=f"Response {response.status} from {response.body()} {response.url}",
            attachment_type=allure.attachment_type.TEXT,
        )
