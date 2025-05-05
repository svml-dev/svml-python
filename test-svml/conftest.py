import pytest
from svml.client import SVMLClient

@pytest.fixture(scope="session")
def client():
    c = SVMLClient()
    c.authenticate()
    return c 