import os
import pytest
from svml.schemas.analyze import ALL_ANALYZE_DIMENSIONS
import logging

# Set up logger
logger = logging.getLogger(__name__)

FIXTURE_DIR = os.path.join(os.path.dirname(__file__), 'fixtures')

def load_svml(name):
    with open(os.path.join(FIXTURE_DIR, name), 'r') as f:
        return f.read()
    
def test_analyze_cognitive_divergence(client):
    logger.info(f"[INFO] Testing cognitive divergence")
    svml = load_svml('valid_svml.svml')
    svml_version = '1.2.2'
    model = 'claude-3-5-sonnet-20241022'
    requested_dimensions = ['cognitive_divergence']
    response = client.analyze(svml=svml, svml_version=svml_version, model=model, dimensions=requested_dimensions)
    assert isinstance(response, dict) or hasattr(response, 'dimensions')
    if isinstance(response, dict):
        assert 'svml_version' in response
        assert 'svml_credits' in response
    else:
        assert hasattr(response, 'svml_version')
        assert hasattr(response, 'svml_credits')
    dimensions = response['dimensions'] if isinstance(response, dict) else response.dimensions
    assert isinstance(dimensions, dict)
    assert set(dimensions.keys()) == set(requested_dimensions)
    assert 'overall_score' in (response if isinstance(response, dict) else response.__dict__)
    assert 'verdict' in (response if isinstance(response, dict) else response.__dict__)
    assert not hasattr(response, 'usage')
    assert not hasattr(response.dimensions, 'usage')

def test_analyze_compression_signature(client):
    logger.info(f"[INFO] Testing compression signature")
    svml = load_svml('valid_svml.svml')
    svml_version = '1.2.2'
    model = 'claude-3-5-sonnet-20241022'
    requested_dimensions = ['compression_signature']
    response = client.analyze(svml=svml, svml_version=svml_version, model=model, dimensions=requested_dimensions)
    assert isinstance(response, dict) or hasattr(response, 'dimensions')
    if isinstance(response, dict):
        assert 'svml_version' in response
        assert 'svml_credits' in response
    else:
        assert hasattr(response, 'svml_version')
        assert hasattr(response, 'svml_credits')
    dimensions = response['dimensions'] if isinstance(response, dict) else response.dimensions
    assert isinstance(dimensions, dict)
    assert set(dimensions.keys()) == set(requested_dimensions)
    assert 'overall_score' in (response if isinstance(response, dict) else response.__dict__)
    assert 'verdict' in (response if isinstance(response, dict) else response.__dict__)
    assert not hasattr(response, 'usage')
    assert not hasattr(response.dimensions, 'usage')

def test_analyze_metaphor_anchoring(client):
    logger.info(f"[INFO] Testing metaphor anchoring")
    svml = load_svml('valid_svml.svml')
    svml_version = '1.2.2'
    model = 'claude-3-5-sonnet-20241022'
    requested_dimensions = ['metaphor_anchoring']
    response = client.analyze(svml=svml, svml_version=svml_version, model=model, dimensions=requested_dimensions)
    assert isinstance(response, dict) or hasattr(response, 'dimensions')
    if isinstance(response, dict):
        assert 'svml_version' in response
        assert 'svml_credits' in response
    else:
        assert hasattr(response, 'svml_version')
        assert hasattr(response, 'svml_credits')
    dimensions = response['dimensions'] if isinstance(response, dict) else response.dimensions
    assert isinstance(dimensions, dict)
    assert set(dimensions.keys()) == set(requested_dimensions)
    assert 'overall_score' in (response if isinstance(response, dict) else response.__dict__)
    assert 'verdict' in (response if isinstance(response, dict) else response.__dict__)
    assert not hasattr(response, 'usage')
    assert not hasattr(response.dimensions, 'usage')

def test_analyze_prompt_form_alignment(client):
    logger.info(f"[INFO] Testing prompt form alignment")
    svml = load_svml('valid_svml.svml')
    svml_version = '1.2.2'
    model = 'claude-3-5-sonnet-20241022'
    requested_dimensions = ['prompt_form_alignment']
    response = client.analyze(svml=svml, svml_version=svml_version, model=model, dimensions=requested_dimensions)
    assert isinstance(response, dict) or hasattr(response, 'dimensions')
    if isinstance(response, dict):
        assert 'svml_version' in response
        assert 'svml_credits' in response
    else:
        assert hasattr(response, 'svml_version')
        assert hasattr(response, 'svml_credits')
    dimensions = response['dimensions'] if isinstance(response, dict) else response.dimensions
    assert isinstance(dimensions, dict)
    assert set(dimensions.keys()) == set(requested_dimensions)
    assert 'overall_score' in (response if isinstance(response, dict) else response.__dict__)
    assert 'verdict' in (response if isinstance(response, dict) else response.__dict__)
    assert not hasattr(response, 'usage')
    assert not hasattr(response.dimensions, 'usage')

def test_analyze_author_trace(client):
    logger.info(f"[INFO] Testing author trace")
    svml = load_svml('valid_svml.svml')
    svml_version = '1.2.2'
    model = 'claude-3-5-sonnet-20241022'
    requested_dimensions = ['author_trace']
    response = client.analyze(svml=svml, svml_version=svml_version, model=model, dimensions=requested_dimensions)
    assert isinstance(response, dict) or hasattr(response, 'dimensions')
    if isinstance(response, dict):
        assert 'svml_version' in response
        assert 'svml_credits' in response
    else:
        assert hasattr(response, 'svml_version')
        assert hasattr(response, 'svml_credits')
    dimensions = response['dimensions'] if isinstance(response, dict) else response.dimensions
    assert isinstance(dimensions, dict)
    assert set(dimensions.keys()) == set(requested_dimensions)
    assert 'overall_score' in (response if isinstance(response, dict) else response.__dict__)
    assert 'verdict' in (response if isinstance(response, dict) else response.__dict__)
    assert not hasattr(response, 'usage')
    assert not hasattr(response.dimensions, 'usage')

def test_analyze_ambiguity_resolution(client):
    logger.info(f"[INFO] Testing ambiguity resolution")
    svml = load_svml('valid_svml.svml')
    svml_version = '1.2.2'
    model = 'claude-3-5-sonnet-20241022'
    requested_dimensions = ['ambiguity_resolution']
    response = client.analyze(svml=svml, svml_version=svml_version, model=model, dimensions=requested_dimensions)
    assert isinstance(response, dict) or hasattr(response, 'dimensions')
    if isinstance(response, dict):
        assert 'svml_version' in response
        assert 'svml_credits' in response
    else:
        assert hasattr(response, 'svml_version')
        assert hasattr(response, 'svml_credits')
    dimensions = response['dimensions'] if isinstance(response, dict) else response.dimensions
    assert isinstance(dimensions, dict)
    assert set(dimensions.keys()) == set(requested_dimensions)
    assert 'overall_score' in (response if isinstance(response, dict) else response.__dict__)
    assert 'verdict' in (response if isinstance(response, dict) else response.__dict__)
    assert not hasattr(response, 'usage')
    assert not hasattr(response.dimensions, 'usage')

def test_analyze_two_dimensions(client):
    logger.info(f"[INFO] Testing two dimensions")
    svml = load_svml('valid_svml.svml')
    svml_version = '1.2.2'
    model = 'claude-3-5-sonnet-20241022'
    requested_dimensions = ['cognitive_divergence', 'compression_signature']
    response = client.analyze(svml=svml, svml_version=svml_version, model=model, dimensions=requested_dimensions)
    assert isinstance(response, dict) or hasattr(response, 'dimensions')
    if isinstance(response, dict):
        assert 'svml_version' in response
        assert 'svml_credits' in response
    else:
        assert hasattr(response, 'svml_version')
        assert hasattr(response, 'svml_credits')
    dimensions = response['dimensions'] if isinstance(response, dict) else response.dimensions
    assert isinstance(dimensions, dict)
    assert set(dimensions.keys()) == set(requested_dimensions)
    assert 'overall_score' in (response if isinstance(response, dict) else response.__dict__)
    assert 'verdict' in (response if isinstance(response, dict) else response.__dict__)
    assert not hasattr(response, 'usage')
    assert not hasattr(response.dimensions, 'usage')


def test_analyze_all_dimensions_claude35sonnet(client):
    logger.info(f"[INFO] Testing all dimensions with claude-3-5-sonnet-20241022")
    svml = load_svml('valid_svml.svml')
    svml_version = '1.2.2'
    model = 'claude-3-5-sonnet-20241022'
    requested_dimensions = ALL_ANALYZE_DIMENSIONS
    response = client.analyze(svml=svml, svml_version=svml_version, model=model, dimensions=requested_dimensions)
    assert isinstance(response, dict) or hasattr(response, 'dimensions')
    if isinstance(response, dict):
        assert 'svml_version' in response
        assert 'svml_credits' in response
    else:
        assert hasattr(response, 'svml_version')
        assert hasattr(response, 'svml_credits')
    dimensions = response['dimensions'] if isinstance(response, dict) else response.dimensions
    assert isinstance(dimensions, dict)
    assert set(dimensions.keys()) == set(requested_dimensions)
    assert 'overall_score' in (response if isinstance(response, dict) else response.__dict__)
    assert 'verdict' in (response if isinstance(response, dict) else response.__dict__)
    assert not hasattr(response, 'usage')
    assert not hasattr(response.dimensions, 'usage')

# def test_analyze_all_dimensions_gpt4o_mini(client):
#     logger.info(f"[INFO] Testing all dimensions with gpt-4o-mini")
#     svml = load_svml('valid_svml.svml')
#     svml_version = '1.2.2'
#     #model = 'claude-3-5-sonnet-20241022'
#     model = 'gpt-4o-mini'
#     requested_dimensions = ALL_ANALYZE_DIMENSIONS
#     response = client.analyze(svml=svml, svml_version=svml_version, model=model, dimensions=requested_dimensions)
#     assert isinstance(response, dict) or hasattr(response, 'dimensions')
#     if isinstance(response, dict):
#         assert 'svml_version' in response
#         assert 'svml_credits' in response
#     else:
#         assert hasattr(response, 'svml_version')
#         assert hasattr(response, 'svml_credits')
#     dimensions = response['dimensions'] if isinstance(response, dict) else response.dimensions
#     assert isinstance(dimensions, dict)
#     assert set(dimensions.keys()) == set(requested_dimensions)
#     assert 'overall_score' in (response if isinstance(response, dict) else response.__dict__)
#     assert 'verdict' in (response if isinstance(response, dict) else response.__dict__)
#     assert not hasattr(response, 'usage')
#     assert not hasattr(response.dimensions, 'usage')
