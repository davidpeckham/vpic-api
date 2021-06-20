from logging import exception
from typing import Optional
from requests.models import Response


def handle_error_response(resp: Response):

    HTTP_ERRORS = {
        400: InvalidRequest,
        404: MethodNotFound,
        429: TooManyRequests,
        500: InternalError,
        503: ServiceUnavailable,
    }

    if resp.headers.get('content-type', 'application/json') == 'application/json':
        error = resp.json()
        message = error.get("message")
        detail = error.get("messageDetail")
    else:
        error = ""
        message = ""
        detail = ""

    exc = HTTP_ERRORS.get(resp.status_code, VPICError)
    if detail.startswith("The parameters dictionary"):
        exc = InvalidParameters

    raise exc(message=message, detail=detail, response=resp)



class VPICError(Exception):
    """Base class for vPIC API client exceptions.

    Attributes:
        message : Human readable string describing the exception.
        detail: A more detailed or specific description of the exception.
        response: The ``requests.models.Response`` from the vPIC API.

    """

    message: str = "An unknown error occurred"
    detail: Optional[str] = None
    response: Optional[Response] = None

    def __init__(
        self,
        message: Optional[str] = None,
        detail: Optional[str] = None,
        response: Optional[Response] = None,
    ):
        self.response = response
        if message:
            self.message = message
        if detail:
            self.detail = detail

    def __str__(self):
        return self.message


class InvalidRequest(VPICError):
    pass


class MethodNotFound(VPICError):
    """Method not found in vPIC API."""

    pass


class InvalidParameters(VPICError):
    """You passed an invalid parameter value."""

    pass


class TooManyRequests(VPICError):
    """You made too many requests

    See the Retry-After header for advice about how long to wait
    before submitting another request.

    """

    pass


class InternalError(VPICError):
    """An error occurred in the service"""

    pass


class ServiceUnavailable(VPICError):
    """The service is not available, and may be down for maintenance."""

    pass


class ParseError(VPICError):
    pass
