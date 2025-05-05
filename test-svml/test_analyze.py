import os
import pytest
from svml.endpoints.analyze import ALL_ANALYZE_DIMENSIONS

FIXTURE_DIR = os.path.join(os.path.dirname(__file__), 'fixtures')

def load_svml(name):
    with open(os.path.join(FIXTURE_DIR, name), 'r') as f:
        return f.read()

def test_analyze_cognitive_divergence(client):
    svml = load_svml('valid_svml.svml')
    svml_version = '1.2.2'
    model = 'claude-3-5-sonnet-20241022'
    dimension = 'cognitive_divergence'
    response = client.analyze(svml=svml, svml_version=svml_version, model=model, dimensions=[dimension])
    assert isinstance(response, dict) or hasattr(response, 'dimensions')
    dimensions = response['dimensions'] if isinstance(response, dict) else response.dimensions
    assert isinstance(dimensions, dict)
    assert list(dimensions.keys()) == [dimension]
    assert 'overall_score' in (response if isinstance(response, dict) else response.__dict__)
    assert 'verdict' in (response if isinstance(response, dict) else response.__dict__)

def test_analyze_compression_signature(client):
    svml = load_svml('valid_svml.svml')
    svml_version = '1.2.2'
    model = 'claude-3-5-sonnet-20241022'
    dimension = 'compression_signature'
    response = client.analyze(svml=svml, svml_version=svml_version, model=model, dimensions=[dimension])
    assert isinstance(response, dict) or hasattr(response, 'dimensions')
    dimensions = response['dimensions'] if isinstance(response, dict) else response.dimensions
    assert isinstance(dimensions, dict)
    assert list(dimensions.keys()) == [dimension]
    assert 'overall_score' in (response if isinstance(response, dict) else response.__dict__)
    assert 'verdict' in (response if isinstance(response, dict) else response.__dict__)

def test_analyze_metaphor_anchoring(client):
    svml = load_svml('valid_svml.svml')
    svml_version = '1.2.2'
    model = 'claude-3-5-sonnet-20241022'
    dimension = 'metaphor_anchoring'
    response = client.analyze(svml=svml, svml_version=svml_version, model=model, dimensions=[dimension])
    assert isinstance(response, dict) or hasattr(response, 'dimensions')
    dimensions = response['dimensions'] if isinstance(response, dict) else response.dimensions
    assert isinstance(dimensions, dict)
    assert list(dimensions.keys()) == [dimension]
    assert 'overall_score' in (response if isinstance(response, dict) else response.__dict__)
    assert 'verdict' in (response if isinstance(response, dict) else response.__dict__)

def test_analyze_prompt_form_alignment(client):
    svml = load_svml('valid_svml.svml')
    svml_version = '1.2.2'
    model = 'claude-3-5-sonnet-20241022'
    dimension = 'prompt_form_alignment'
    response = client.analyze(svml=svml, svml_version=svml_version, model=model, dimensions=[dimension])
    assert isinstance(response, dict) or hasattr(response, 'dimensions')
    dimensions = response['dimensions'] if isinstance(response, dict) else response.dimensions
    assert isinstance(dimensions, dict)
    assert list(dimensions.keys()) == [dimension]
    assert 'overall_score' in (response if isinstance(response, dict) else response.__dict__)
    assert 'verdict' in (response if isinstance(response, dict) else response.__dict__)

def test_analyze_author_trace(client):
    svml = load_svml('valid_svml.svml')
    svml_version = '1.2.2'
    model = 'claude-3-5-sonnet-20241022'
    dimension = 'author_trace'
    response = client.analyze(svml=svml, svml_version=svml_version, model=model, dimensions=[dimension])
    assert isinstance(response, dict) or hasattr(response, 'dimensions')
    dimensions = response['dimensions'] if isinstance(response, dict) else response.dimensions
    assert isinstance(dimensions, dict)
    assert list(dimensions.keys()) == [dimension]
    assert 'overall_score' in (response if isinstance(response, dict) else response.__dict__)
    assert 'verdict' in (response if isinstance(response, dict) else response.__dict__)

def test_analyze_ambiguity_resolution(client):
    svml = load_svml('valid_svml.svml')
    svml_version = '1.2.2'
    model = 'claude-3-5-sonnet-20241022'
    dimension = 'ambiguity_resolution'
    response = client.analyze(svml=svml, svml_version=svml_version, model=model, dimensions=[dimension])
    assert isinstance(response, dict) or hasattr(response, 'dimensions')
    dimensions = response['dimensions'] if isinstance(response, dict) else response.dimensions
    assert isinstance(dimensions, dict)
    assert list(dimensions.keys()) == [dimension]
    assert 'overall_score' in (response if isinstance(response, dict) else response.__dict__)
    assert 'verdict' in (response if isinstance(response, dict) else response.__dict__)

# Add more tests for other dimensions as needed, following the same pattern. 