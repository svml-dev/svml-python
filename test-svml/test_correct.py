import json
import os
import pytest

FIXTURE_DIR = os.path.join(os.path.dirname(__file__), 'fixtures')

def load_fixture(name):
    with open(os.path.join(FIXTURE_DIR, name), 'r') as f:
        return json.load(f)

# Test for correct endpoint using the validate_invalid_svml.json fixture
def test_correct_with_invalid_svml(client):
    fixture = load_fixture('validate_invalid_svml.json')
    response = client.correct(fixture)
    print("Correct response:", response)
    from svml.schemas.correct import CorrectResponse
    assert isinstance(response, CorrectResponse)
    assert hasattr(response, 'svml_version')
    assert hasattr(response, 'svml_credits')
    assert hasattr(response, 'output')
    assert hasattr(response, 'usage')
    assert isinstance(response.output, dict)
    assert 'svml' in response.output
    
    
    