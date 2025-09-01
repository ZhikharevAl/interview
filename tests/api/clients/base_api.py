from tests.utils.http_client import HTTPClient


class BaseAPI:
    """
    The base class for all API clients.

    Stores an instance of the HTTP client for executing requests.
    """

    def __init__(self, client: HTTPClient) -> None:
        """Initializes the BaseAPI class."""
        self.http: HTTPClient = client
