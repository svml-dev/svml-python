import json
import os
import pytest

FIXTURE_DIR = os.path.join(os.path.dirname(__file__), 'fixtures')

def load_fixture(name):
    with open(os.path.join(FIXTURE_DIR, name), 'r') as f:
        return json.load(f)

def load_svml(name):
    with open(os.path.join(FIXTURE_DIR, name), 'r') as f:
        return f.read()

def test_validate_valid(client):
    svml = load_svml('valid_svml.svml')
    svml_version = '1.2.2'
    request_data = {'svml': svml, 'svml_version': svml_version}
    print("--------------------------------")
    response = client.validate(**request_data)
    assert isinstance(response, dict) or hasattr(response, 'output')
    # Assert top-level svml_version and svml_credits
    if isinstance(response, dict):
        assert 'svml_version' in response
        assert 'svml_credits' in response
    else:
        assert hasattr(response, 'svml_version')
        assert hasattr(response, 'svml_credits')
    # Optionally, check response['output'] for expected structure

def test_validate_invalid(client):
    svml = load_svml('invalid_svml.svml')
    svml_version = '1.2.2'
    request_data = {'svml': svml, 'svml_version': svml_version}
    print("--------------------------------")
    response = client.validate(**request_data)
    assert isinstance(response, dict) or hasattr(response, 'output')
    # Assert top-level svml_version and svml_credits
    if isinstance(response, dict):
        assert 'svml_version' in response
        assert 'svml_credits' in response
    else:
        assert hasattr(response, 'svml_version')
        assert hasattr(response, 'svml_credits')
    # Optionally, check response['output'] for expected structure 