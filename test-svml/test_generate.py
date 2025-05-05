import json
import os
import pytest

FIXTURE_DIR = os.path.join(os.path.dirname(__file__), 'fixtures')

def load_fixture(name):
    with open(os.path.join(FIXTURE_DIR, name), 'r') as f:
        return json.load(f)

def load_prompt(name):
    with open(os.path.join(FIXTURE_DIR, name), 'r') as f:
        return f.read()

def test_generate_svml_1(client):
    # Use a real prompt/context from fixture
    context = load_prompt('generate_svml_1.svml') if os.path.exists(os.path.join(FIXTURE_DIR, 'generate_svml_1.svml')) else "In the modern workplace, collaboration between teams is essential for innovation, yet communication barriers often arise due to differing priorities, technical jargon, and organizational silos."
    svml_version = '1.2.2'
    model = 'gpt-4.1-mini'
    response = client.generate(context=context, svml_version=svml_version, model=model)
    assert isinstance(response, dict) or hasattr(response, 'output')
    output = response['output'] if isinstance(response, dict) else response.output
    assert 'svml' in output and isinstance(output['svml'], str)


def test_generate_svml_2(client):
    # Use a different prompt/context from fixture if available
    context = load_prompt('generate_svml_2.svml') if os.path.exists(os.path.join(FIXTURE_DIR, 'generate_svml_2.svml')) else "Describe the process of creative problem-solving in a team environment."
    svml_version = '1.2.2'
    model = 'claude-3-5-sonnet-20241022'
    response = client.generate(context=context, svml_version=svml_version, model=model)
    assert isinstance(response, dict) or hasattr(response, 'output')
    output = response['output'] if isinstance(response, dict) else response.output
    assert 'svml' in output and isinstance(output['svml'], str) 