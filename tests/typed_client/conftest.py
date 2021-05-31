import pytest

from vpic import TypedClient


@pytest.fixture(scope="session")
def typed_client() -> TypedClient:
    return TypedClient(unknown='RAISE')
