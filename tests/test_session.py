import pytest
from requests import Request

from vpic.session import VpicAPISession


@pytest.fixture
def fake_request():
    return Request("GET", "http://someurl/")


def test_request_headers(fake_request):
    s = VpicAPISession()
    r = s.prepare_request(fake_request)

    assert r.headers["Accept-Charset"] == "utf-8"
    # assert r.headers["Content-Type"] == "text/plain"
