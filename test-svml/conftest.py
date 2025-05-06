import pytest
from svml.client import SVMLClient
import logging
import os

@pytest.fixture(scope="session")
def client():
    c = SVMLClient()
    if os.environ.get("SVML_API_KEY"):
        c.authenticate()
    return c 

# Configure logging for pytest
def pytest_configure(config):
    # Set up basic logging configuration
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # You can also set specific loggers to different levels if needed
    # For example:
    logging.getLogger('svml').setLevel(logging.INFO) 