import json
import os
import pytest

FIXTURE_DIR = os.path.join(os.path.dirname(__file__), 'fixtures')

def load_fixture(name):
    with open(os.path.join(FIXTURE_DIR, name), 'r') as f:
        return json.load(f)

def test_compare_svml_only(client):
    generate1 = load_fixture('generate_1.json')
    generate2 = load_fixture('generate_2.json')
    svml_a = generate1['output']['svml']
    model_a = generate1['metadata']['model']
    svml_b = generate2['output']['svml']
    model_b = generate2['metadata']['model']
    original_context = generate1['input']['context']
    svml_version = generate1.get('svml_version', '1.2.2')
    model = 'gpt-4.1-mini'
    request_data = {
        'svml_a': svml_a,
        'model_a': model_a,
        'svml_b': svml_b,
        'model_b': model_b,
        'original_context': original_context,
        'svml_version': svml_version,
        'model': model,
    }
    response = client.compare(**request_data)
    assert isinstance(response, dict) or hasattr(response, 'output')
    # Optionally, check response['output'] for expected structure

def test_compare_with_justifications(client):
    generate1 = load_fixture('generate_1.json')
    generate2 = load_fixture('generate_2.json')
    original_context = generate1['input']['context']
    svml_version = generate1.get('svml_version', '1.2.2')
    model = 'gpt-4.1-mini'
    request_data = {
        'generate_api_output_a': generate1,
        'generate_api_output_b': generate2,
        'original_context': original_context,
        'svml_version': svml_version,
        'model': model,
    }
    response = client.compare(**request_data)
    assert isinstance(response, dict) or hasattr(response, 'output')
    # Optionally, check response['output'] for expected structure 