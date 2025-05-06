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
    """Test direct SVML refinement by extracting SVML and context from generate_1.json"""
    # Load the generate fixture
    generate_output = load_fixture('generate_1.json')
    
    # Extract the context and SVML from generate_1.json
    original_context = generate_output['input']['context']
    svml = generate_output['output']['svml']
    
    # Create request with required parameters for direct SVML refinement
    request_data = {
        'svml': svml,
        'original_context': original_context,
        'user_additional_context': 'Improve the hierarchical structure of this SVML',
        'model': 'gpt-4.1-mini',
        'svml_version': '1.2.2'
    }
    
    # Filter to only the allowed keys
    filtered = filter_keys(request_data, REFINE_SVML_KEYS)
    
    # Call refine
    response = client.refine(**filtered)
    
    # Verify response
    assert isinstance(response, dict) or hasattr(response, 'output')
    # Assert top-level svml_version and svml_credits
    if isinstance(response, dict):
        assert 'svml_version' in response
        assert 'svml_credits' in response
    else:
        assert hasattr(response, 'svml_version')
        assert hasattr(response, 'svml_credits')
    # Check that the response contains SVML
    if hasattr(response, 'output'):
        assert 'svml' in response.output
    elif isinstance(response, dict) and 'output' in response:
        assert 'svml' in response['output']

def test_refine_from_generate(client):
    """Test refineFromGenerate with a generate API output"""
    # Load the generate fixture directly
    generate_output = load_fixture('generate_1.json')
    
    # Create request with required parameters
    request_data = {
        'generate_api_output': generate_output,
        'user_additional_context': 'Improve the SVML so that it has more depth',
        'model': 'gpt-4.1-mini',
        'svml_version': '1.2.2'
    }
    
    # Filter to only the allowed keys
    filtered = filter_keys(request_data, REFINE_FROM_GENERATE_KEYS)
    
    # Call refineFromGenerate
    response = client.refineFromGenerate(**filtered)
    
    # Verify response
    assert isinstance(response, dict) or hasattr(response, 'output')
    
    # Check that the response contains SVML
    if hasattr(response, 'output'):
        assert 'svml' in response.output
    elif isinstance(response, dict) and 'output' in response:
        assert 'svml' in response['output']

def test_refine_from_compare(client):
    """Test refineFromCompare with output from compareFromGenerate"""
    # Load the compare_from_generate fixture directly
    compare_output = load_fixture('compare_from_generate.json')
    
    # Create request with required parameters for refineFromCompare
    request_data = {
        'compare_api_output': compare_output,
        'user_additional_context': 'Refine the SVML based on the comparison analysis',
        'model': 'gpt-4.1-mini', 
        'svml_version': '1.2.2'
    }
    
    # Filter to only the allowed keys
    filtered = filter_keys(request_data, REFINE_FROM_COMPARE_KEYS)
    
    # Call refineFromCompare
    response = client.refineFromCompare(**filtered)
    
    # Verify response
    assert isinstance(response, dict) or hasattr(response, 'output')
    
    # Check that the response contains SVML
    if hasattr(response, 'output'):
        assert 'svml' in response.output
    elif isinstance(response, dict) and 'output' in response:
        assert 'svml' in response['output'] 