import json
import os
import pytest
from svml.schemas.common import StandardLLMSettingsParams
from svml.schemas.correct import CorrectResponse

FIXTURE_DIR = os.path.join(os.path.dirname(__file__), 'fixtures')

def load_fixture(name):
    with open(os.path.join(FIXTURE_DIR, name), 'r') as f:
        return json.load(f)

# Test for correct endpoint using the validate_invalid_svml.json fixture
def test_correct_with_invalid_svml(client):
    fixture = load_fixture('validate_invalid_svml.json')
    settings = StandardLLMSettingsParams(model='gpt-4.1-mini', svml_version='1.2.2')
    
    response = client.correct(validate_api_output=fixture, settings=settings)
    print("Correct response:", response)
    assert isinstance(response, CorrectResponse)
    assert hasattr(response, 'svml_version')
    assert hasattr(response, 'svml_credits')
    assert hasattr(response, 'output')
    assert isinstance(response.output, dict)
    assert 'svml' in response.output
    assert not hasattr(response.output, 'usage')
    assert not hasattr(response, 'usage')
    
    
    
    