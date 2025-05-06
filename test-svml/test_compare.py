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
    svml_b = generate2['output']['svml']
    original_context = generate1['input']['context']
    svml_version = generate1.get('svml_version', '1.2.2')
    model = 'gpt-4.1-mini'
    
    # Use the correct method signature for compare
    response = client.compare(
        original_context=original_context,
        svml_a=svml_a,
        svml_b=svml_b,
        model=model,
        svml_version=svml_version
    )
    
    assert isinstance(response, dict) or hasattr(response, 'output')
    # Assert top-level svml_version and svml_credits
    if isinstance(response, dict):
        assert 'svml_version' in response
        assert 'svml_credits' in response
    else:
        assert hasattr(response, 'svml_version')
        assert hasattr(response, 'svml_credits')
    
    assert not hasattr(response, 'usage')
    assert not hasattr(response.output, 'usage')
    

def test_compare_with_justifications(client):
    generate1 = load_fixture('generate_1.json')
    generate2 = load_fixture('generate_2.json')
    svml_version = generate1.get('svml_version', '1.2.2')
    model = 'gpt-4.1-mini'
    
    # Use the correct method for comparing from generate outputs
    response = client.compareFromGenerate(
        generate_api_output_a=generate1,
        generate_api_output_b=generate2,
        model=model,
        svml_version=svml_version
    )
    
    assert isinstance(response, dict) or hasattr(response, 'output')
    # Assert top-level svml_version and svml_credits
    if isinstance(response, dict):
        assert 'svml_version' in response
        assert 'svml_credits' in response
    else:
        assert hasattr(response, 'svml_version')
        assert hasattr(response, 'svml_credits')
    
    assert not hasattr(response, 'usage')
    assert not hasattr(response.output, 'usage')
    