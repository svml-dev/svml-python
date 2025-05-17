import json
import os
import pytest
from svml.schemas.common import StandardLLMSettingsParams

FIXTURE_DIR = os.path.join(os.path.dirname(__file__), 'fixtures')

def load_fixture(name):
    with open(os.path.join(FIXTURE_DIR, name), 'r') as f:
        return json.load(f)

def load_prompt(name):
    with open(os.path.join(FIXTURE_DIR, name), 'r') as f:
        return f.read()

def test_generate_svml_1(client):
    # Use a real prompt/context from fixture
    context = load_prompt('start_prompt_1.md') if os.path.exists(os.path.join(FIXTURE_DIR, 'start_prompt_1.md')) else "In the modern workplace, collaboration between teams is essential for innovation, yet communication barriers often arise due to differing priorities, technical jargon, and organizational silos."
    settings = StandardLLMSettingsParams(model='gpt-4.1-mini', svml_version='1.2.2')
    response = client.generate(context=context, settings=settings)
    assert isinstance(response, dict) or hasattr(response, 'output')
    # Assert top-level svml_version and svml_credits
    if isinstance(response, dict):
        assert 'svml_version' in response
        assert 'svml_credits' in response
    else:
        assert hasattr(response, 'svml_version')
        assert hasattr(response, 'svml_credits')
    output = response['output'] if isinstance(response, dict) else response.output
    assert 'svml' in output and isinstance(output['svml'], str)
    assert not hasattr(response, 'usage')
    assert not hasattr(response, 'output') or not hasattr(response.output, 'usage')

def test_generate_svml_2(client):
    # Use a different prompt/context from fixture if available
    context = load_prompt('start_prompt_1.md') if os.path.exists(os.path.join(FIXTURE_DIR, 'start_prompt_1.md')) else "In the modern workplace, collaboration between teams is essential for innovation, yet communication barriers often arise due to differing priorities, technical jargon, and organizational silos."
    settings = StandardLLMSettingsParams(model='claude-3-5-sonnet-20241022', svml_version='1.2.2')
    response = client.generate(context=context, settings=settings)
    assert isinstance(response, dict) or hasattr(response, 'output')
    # Assert top-level svml_version and svml_credits
    if isinstance(response, dict):
        assert 'svml_version' in response
        assert 'svml_credits' in response
    else:
        assert hasattr(response, 'svml_version')
        assert hasattr(response, 'svml_credits')
    output = response['output'] if isinstance(response, dict) else response.output
    assert 'svml' in output and isinstance(output['svml'], str) 
    assert not hasattr(response, 'usage')
    assert not hasattr(response, 'output') or not hasattr(response.output, 'usage')