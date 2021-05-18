import json
from pathlib import Path

import pytest
import responses as responses_

from vpic import Client


@pytest.fixture(scope="session")
def vpic() -> Client:
    return Client()


@pytest.fixture(scope="session")
def responses():

    endpoints = {}

    def _request_callback():
        def _handle(request):
            response_file = endpoints[request.url]["response_file"]
            with Path(response_file).open(encoding='utf-8') as fp:
                resp = json.load(fp)
            return (
                resp["status"],
                {},
                json.dumps(resp["content"]),
            )

        return _handle

    def _response_callback(resp):
        # placeholder
        resp.callback_processed = True
        return resp

    with responses_.RequestsMock(
        assert_all_requests_are_fired=False, response_callback=_response_callback
    ) as requests_mock:

        response_files = list(Path("tests").glob("**/*.json"))
        for rf in response_files:
            with rf.open(encoding='utf-8') as fp:
                resp = json.load(fp)
                endpoints[resp["url"]] = {
                    "method": resp.get("method", "GET"),
                    "status": resp["status"],
                    "response_file": str(rf),
                }

        for url, spec in endpoints.items():
            requests_mock.add_callback(
                spec["method"],
                url,
                callback=_request_callback(),
            )
        yield requests_mock
