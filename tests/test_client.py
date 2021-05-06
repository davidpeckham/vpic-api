from vpic.client import BaseAPI


def test_init():
    c = BaseAPI(host="http://somehost/")

    assert c.host == "http://somehost/"


def test_url():
    c = BaseAPI(host="http://somehost")

    assert c.url == "http://somehost"
