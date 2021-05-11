import pytest
from vpic.typed_client import TypedClient


@pytest.fixture(scope="session")
def typed_client() -> TypedClient:
    return TypedClient()
