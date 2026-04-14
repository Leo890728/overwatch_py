class APIError(Exception):
    def __init__(self, message: str, status_code: int, response=None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class BadRequestError(APIError):
    """400 Bad Request Error"""


class NotFoundError(APIError):
    """404 Not Found (hero or player)"""


class ValidationError(APIError):
    """422 Validation Error"""


class APIRateLimitError(APIError):
    """429 API Rate Limit Error"""


class InternalServerError(APIError):
    """500 Internal Server Error"""


class BlizzardRateLimitError(APIError):
    """503 Blizzard Rate Limit Error"""


class BlizzardServerError(APIError):
    """504 Blizzard Server Error"""