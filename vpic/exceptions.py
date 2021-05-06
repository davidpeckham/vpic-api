def handle_error_response(resp):

    HTTP_ERRORS = {
        400: InvalidRequest,
        404: MethodNotFound,
        429: TooManyRequests,
        500: InternalError,
        503: ServiceUnavailable,
    }

    error = resp.json()
    message = error.get("message")
    detail = error.get("messageDetail")

    exc = HTTP_ERRORS.get(resp.status_code, VpicAPIError)

    if resp.status_code == 400 and detail.startswith("The parameters dictionary"):
        exc = InvalidParameters

    raise exc(message=message, detail=detail, response=resp)


class VpicAPIError(Exception):
    message = "An unknown error occurred"
    detail = None
    response = None

    def __init__(self, message=None, detail=None, response=None):
        self.response = response
        if message:
            self.message = message
        if detail:
            self.detail = detail

    def __str__(self):
        return self.message


class InvalidRequest(VpicAPIError):
    pass


class MethodNotFound(VpicAPIError):
    pass


class InvalidParameters(VpicAPIError):
    pass


class TooManyRequests(VpicAPIError):
    # see the Retry-After header
    pass


class InternalError(VpicAPIError):
    pass


class ServiceUnavailable(VpicAPIError):
    # see the Retry-After header
    pass


class ParseError(VpicAPIError):
    pass
