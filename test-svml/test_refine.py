import json
import os
import pytest

FIXTURE_DIR = os.path.join(os.path.dirname(__file__), 'fixtures')

def load_fixture(name):
    with open(os.path.join(FIXTURE_DIR, name), 'r') as f:
        return json.load(f)

def filter_keys(d, allowed):
    return {k: v for k, v in d.items() if k in allowed}

# Define the allowed keys for each refine mode
REFINE_SVML_KEYS = {'svml', 'original_context', 'user_additional_context', 'model', 'svml_version'}
REFINE_FROM_GENERATE_KEYS = {'generate_api_output', 'original_context', 'user_additional_context', 'model', 'svml_version'}
REFINE_FROM_COMPARE_KEYS = {'compare_api_output', 'original_context', 'user_additional_context', 'model', 'svml_version'}

def test_refine_svml(client):
    fixture = load_fixture('refine_svml.json')
    request_data = fixture.get('request', fixture)
    if 'input' in request_data:
        request_data = request_data['input']
    # Only pass the relevant keys for direct SVML refinement
    filtered = filter_keys(request_data, REFINE_SVML_KEYS)
    response = client.refine(**filtered)
    assert isinstance(response, dict) or hasattr(response, 'output')
    # Optionally, compare response['output'] to fixture.get('expected_output') if present

def test_refine_analysis_a(client):
    fixture = load_fixture('refine_analysis_a.json')
    request_data = fixture.get('request', fixture)
    if 'input' in request_data:
        request_data = request_data['input']
    # Only pass the relevant keys for generate refinement if present, else compare refinement
    if 'generate_api_output' in request_data:
        filtered = filter_keys(request_data, REFINE_FROM_GENERATE_KEYS)
    elif 'compare_api_output' in request_data:
        filtered = filter_keys(request_data, REFINE_FROM_COMPARE_KEYS)
    else:
        filtered = request_data
    response = client.refine(**filtered)
    assert isinstance(response, dict) or hasattr(response, 'output')
    # Optionally, compare response['output'] to fixture.get('expected_output') if present 