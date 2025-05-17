from svml.client import SVMLClient
import os
import pytest
import logging
import traceback
import sys
import requests

print ('\n')

# Set up logger
logger = logging.getLogger(__name__)

def test_client_init():
    # Basic initialization test
    client = SVMLClient()
    expected_api_base = os.environ.get("SVML_API_BASE", "https://api.svml.dev") + "/v1"
    expected_auth_base = os.environ.get("SVML_AUTH_BASE", "https://auth.svml.dev") + "/v1"
    logger.info(f"\napi_base: {client.api_base}")
    logger.info(f"auth_base: {client.auth_base}")
    logger.info(f"Environment variables:")
    logger.info(f"  SVML_API_BASE: {os.environ.get('SVML_API_BASE', '(not set)')}")
    logger.info(f"  SVML_AUTH_BASE: {os.environ.get('SVML_AUTH_BASE', '(not set)')}")
    logger.info(f"  SVML_API_KEY: {'(set)' if os.environ.get('SVML_API_KEY') else '(not set)'}")
    
    assert client.api_base == expected_api_base
    assert client.auth_base == expected_auth_base
    assert client.token is None 

@pytest.mark.skipif(not os.environ.get("SVML_API_KEY"), reason="SVML_API_KEY not set")
def test_client_authentication():
    # Test with API key authentication
    api_key = os.environ.get("SVML_API_KEY")
    try:
        # Check if API endpoints are reachable
        logger.info(f"Checking API connectivity...")
        api_base = os.environ.get("SVML_API_BASE", "https://api.svml.dev")
        auth_base = os.environ.get("SVML_AUTH_BASE", "https://auth.svml.dev")
        
        try:
            # Validate auth endpoint is up (just a HEAD request)
            auth_check = requests.head(f"{auth_base}/health", timeout=5)
            logger.info(f"Auth health check: {auth_check.status_code}")
        except Exception as e:
            logger.error(f"Failed to connect to auth endpoint: {str(e)}")
        
        logger.info(f"Initializing client with API key: {api_key[:5]}...")
        client = SVMLClient(api_key=api_key)
        
        # Authenticate and verify token
        logger.info(f"Attempting authentication...")
        client.authenticate()
        
        # Log token info
        logger.info(f"Authentication successful. Token: {client.token[:10]}...")
        
        # Inspect and log client attributes to find model information
        attrs = [attr for attr in dir(client) if not attr.startswith('_')]
        logger.info(f"Client attributes: {attrs}")
        
        # For models and versions attributes, find what they're called
        model_attrs = []
        for attr in attrs:
            val = getattr(client, attr)
            if isinstance(val, list) and len(val) > 0:
                logger.info(f"List attribute '{attr}': {val[:3]}...")
                model_attrs.append(attr)
        
        # Check that we got a valid JWT token
        assert client.token is not None
        assert len(client.token) > 20  # JWT tokens are typically much longer
        
        logger.info(f"Model-related attributes found: {model_attrs}")
        
        if not model_attrs:
            logger.warning("No model-related attributes found! Authentication may be incomplete.")
    
    except Exception as e:
        logger.error(f"Exception in test_client_authentication: {str(e)}")
        logger.error(traceback.format_exc())
        raise 