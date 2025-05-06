#!/usr/bin/env python
import json
import os
import sys
import re
from svml.client import SVMLClient

# Setup paths
FIXTURE_DIR = os.path.join(os.path.dirname(__file__), 'test-svml', 'fixtures')

def load_env_from_file(filename='.env.local'):
    """Load environment variables from a .env file"""
    try:
        with open(filename, 'r') as f:
            content = f.read()
        for line in content.splitlines():
            if line.strip() and not line.startswith('#'):
                key_value = line.strip().split('=', 1)
                if len(key_value) == 2:
                    key, value = key_value
                    # Remove quotes if present
                    value = re.sub(r'^["\']|["\']$', '', value)
                    os.environ[key] = value
        return True
    except FileNotFoundError:
        print(f"Warning: Environment file {filename} not found.")
        return False

def load_fixture(name):
    with open(os.path.join(FIXTURE_DIR, name), 'r') as f:
        return json.load(f)

def save_fixture(data, name):
    with open(os.path.join(FIXTURE_DIR, name), 'w') as f:
        json.dump(data, f, indent=2)

def main():
    # Load environment variables from .env.local file
    env_files = [
        os.path.join(os.path.dirname(__file__), '.env.local'),
        os.path.join(os.getcwd(), '.env.local')
    ]
    
    api_key = os.environ.get("SVML_API_KEY")
    if not api_key:
        for env_file in env_files:
            if load_env_from_file(env_file):
                print(f"Loaded environment from {env_file}")
                api_key = os.environ.get("SVML_API_KEY")
                if api_key:
                    break
    
    if not api_key:
        print("Error: SVML_API_KEY not found in environment or .env.local files.")
        print("Please set your API key with: export SVML_API_KEY='your-api-key'")
        print("Or create a .env.local file with: SVML_API_KEY=your-api-key")
        sys.exit(1)
    
    # Check if compare_from_generate.json exists
    compare_fixture_path = os.path.join(FIXTURE_DIR, 'compare_from_generate.json')
    if not os.path.exists(compare_fixture_path):
        print(f"Error: {compare_fixture_path} not found.")
        print("Please run create_compare_fixture.py first to generate this file.")
        sys.exit(1)
        
    # Load the compare fixture
    print(f"Loading compare fixture from {compare_fixture_path}")
    compare_output = load_fixture('compare_from_generate.json')
    
    # Initialize the client with API key from environment
    client = SVMLClient(api_key=api_key)
    print(f"Initialized SVMLClient with API key")
    
    try:
        # Call refineFromCompare
        print(f"Calling refineFromCompare...")
        response = client.refineFromCompare(
            compare_api_output=compare_output,
            model="gpt-4.1-mini",  # You can specify a different model if needed
            user_additional_context="Please improve the SVML representation based on the analysis of both versions."
        )
        
        print(f"Received response from refineFromCompare")
        
        # Convert the response to a serializable dictionary if it's an object
        if hasattr(response, '__dict__'):
            response_dict = vars(response)
        else:
            response_dict = response
            
        # Create a test fixture structure
        fixture = {
            "request": {
                "input": {
                    "compare_api_output": compare_output,
                    "model": "gpt-4.1-mini",
                    "user_additional_context": "Please improve the SVML representation based on the analysis of both versions."
                }
            },
            "response": response_dict
        }
            
        # Save the response as a new fixture
        fixture_path = os.path.join(FIXTURE_DIR, 'refine_from_compare.json')
        save_fixture(fixture, 'refine_from_compare.json')
        print(f"Successfully created fixture: {fixture_path}")
        
    except Exception as e:
        print(f"Error calling refineFromCompare: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 