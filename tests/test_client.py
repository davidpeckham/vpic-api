from vpic.client_base import ClientBase


def test_init():
    c = ClientBase(host="http://somehost/")

    assert c.host == "http://somehost/"


def test_url():
    c = ClientBase(host="http://somehost")

    assert c.url == "http://somehost"
