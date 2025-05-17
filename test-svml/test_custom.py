import os
import pytest
from svml import SVMLClient # Corrected import case
from svml.schemas.common import StandardLLMSettingsParams # If settings are applicable
from svml.schemas.custom_prompts import CustomPromptParams # For type hint if needed, client handles instantiation
import uuid # For casting string to UUID if prompt_template_id parameter in method expects UUID object

FIXTURE_DIR = os.path.join(os.path.dirname(__file__), 'fixtures')

def load_prompt(name):
    with open(os.path.join(FIXTURE_DIR, name), 'r') as f:
        return f.read()

# Test for the /custom endpoint
def test_custom_endpoint_with_fixture(client: SVMLClient):
    """
    Tests the /custom endpoint using a prompt_template_id and a context variable
    populated from a fixture file, now including required settings.
    """
    prompt_content = load_prompt('start_prompt_1.md')
    
    prompt_template_id_str = "524d558a-4473-473b-84e5-0dbb9deb21d5"
    
    # Define the required settings
    current_svml_version = "1.2.2"
    settings_obj = StandardLLMSettingsParams(
        svml_version=current_svml_version,
        model="claude-3-7-sonnet-20250219"
    )

    template_vars = {
        "context": prompt_content,
        "svml_version": current_svml_version # This might be redundant if svml_version is primarily from settings
    }
    
    # Call client.custom_prompt with prompt_template_id, template_vars, and settings
    response = client.custom_prompt(
        prompt_template_id=uuid.UUID(prompt_template_id_str), # Ensure UUID type if method expects it
        template_vars=template_vars,
        settings=settings_obj
    )

    assert response is not None, "Response should not be None"
    
    # Standard assertions for SVML responses
    if isinstance(response, dict):
        assert 'svml_version' in response, "Response should contain 'svml_version'"
        assert 'svml_credits' in response, "Response should contain 'svml_credits'"
        output = response.get('output')
    else: # Assuming it's a Pydantic model or similar object
        assert hasattr(response, 'svml_version'), "Response object should have 'svml_version' attribute"
        assert hasattr(response, 'svml_credits'), "Response object should have 'svml_credits' attribute"
        output = getattr(response, 'output', None)

    assert output is not None, "Response should contain 'output'"

    print(f"Custom endpoint response output: {output}") 