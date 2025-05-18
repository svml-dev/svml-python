import json
import os
import pytest
from svml.schemas.common import StandardLLMSettingsParams

FIXTURE_DIR = os.path.join(os.path.dirname(__file__), 'fixtures')

def load_fixture(name):
    with open(os.path.join(FIXTURE_DIR, name), 'r') as f:
        return json.load(f)

# def test_refine_svml(client):
#     """Test direct SVML refinement by extracting SVML and context from generate_1.json"""
#     generate_output = load_fixture('generate_1.json')
#     original_context = generate_output['input']['context']
#     svml = generate_output['output']['svml']
#     user_additional_context = 'Improve the hierarchical structure of this SVML and capture more divergent vectors of thought.'
#     settings_obj = StandardLLMSettingsParams(model='gpt-4.1-mini', svml_version='1.2.2')
    
#     response = client.refine(
#         svml=svml,
#         original_context=original_context,
#         user_additional_context=user_additional_context,
#         settings=settings_obj
#     )
    
#     assert isinstance(response, dict) or hasattr(response, 'output')
#     # Assert top-level svml_version and svml_credits
#     if isinstance(response, dict):
#         assert 'svml_version' in response
#         assert 'svml_credits' in response
#     else:
#         assert hasattr(response, 'svml_version')
#         assert hasattr(response, 'svml_credits')
#     # Check that the response contains SVML
#     if hasattr(response, 'output'):
#         assert 'svml' in response.output
#     elif isinstance(response, dict) and 'output' in response:
#         assert 'svml' in response['output']
#     assert not hasattr(response, 'usage')
#     assert not hasattr(response.output, 'usage')

# def test_refine_from_generate(client):
#     """Test refineFromGenerate with a generate API output"""
#     generate_output = load_fixture('generate_1.json')
#     original_context = generate_output['input']['context'] # Though client method might extract it
#     user_additional_context = 'Improve the SVML so that it has more depth and captures more divergent vectors of thought.'
#     settings_obj = StandardLLMSettingsParams(model='gpt-4.1-mini', svml_version='1.2.2')
        
#     response = client.refineFromGenerate(
#         generate_api_output=generate_output,
#         # original_context=original_context, # client method should handle this
#         user_additional_context=user_additional_context,
#         settings=settings_obj
#     )
    
#     assert isinstance(response, dict) or hasattr(response, 'output')
    
#     # Check that the response contains SVML
#     if hasattr(response, 'output'):
#         assert 'svml' in response.output
#     elif isinstance(response, dict) and 'output' in response:
#         assert 'svml' in response['output']
#     assert not hasattr(response, 'usage')
#     assert not hasattr(response.output, 'usage')

def test_refine_from_compare(client):
    """Test refineFromCompare with output from compareFromGenerate"""
    compare_output = load_fixture('compare_from_generate.json')
    # original_context might be derived by client method from compare_output if available
    user_additional_context = 'Refine the SVML based on the comparison analysis'
    settings_obj = StandardLLMSettingsParams(model='gpt-4.1-mini', svml_version='1.2.2')
    svml_choice_to_refine = 'svml_a' # Example choice
            
    response = client.refineFromCompare(
        compare_api_output=compare_output,
        user_additional_context=user_additional_context,
        settings=settings_obj,
        svml_choice=svml_choice_to_refine
    )
    
    assert isinstance(response, dict) or hasattr(response, 'output')
    
    # Check that the response contains SVML
    if hasattr(response, 'output'):
        assert 'svml' in response.output
    elif isinstance(response, dict) and 'output' in response:
        assert 'svml' in response['output'] 
        
    assert not hasattr(response, 'usage')
    assert not hasattr(response.output, 'usage')