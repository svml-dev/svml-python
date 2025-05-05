from svml.client import SVMLClient
import os

def test_client_init():
    client = SVMLClient()
    expected_api_base = os.environ.get("SVML_API_BASE", "https://api.svml.dev")
    expected_auth_base = os.environ.get("SVML_AUTH_BASE", "https://auth.svml.dev")
    assert client.api_base == expected_api_base
    assert client.auth_base == expected_auth_base
    assert client.token is None 