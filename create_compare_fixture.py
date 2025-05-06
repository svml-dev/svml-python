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
    
    # Load the generate fixtures
    print(f"Loading generate fixtures from {FIXTURE_DIR}")
    generate_1 = load_fixture('generate_1.json')
    generate_2 = load_fixture('generate_2.json')
    
    print(f"Loaded generate_1 (model: {generate_1['metadata']['model']}) and generate_2 (model: {generate_2['metadata']['model']})")
    
    # Initialize the client with API key from environment
    client = SVMLClient(api_key=api_key)
    print(f"Initialized SVMLClient with API key")
    client.authenticate()
    
    try:
        # Call compareFromGenerate
        print(f"Calling compareFromGenerate...")
        response = client.compareFromGenerate(
            generate_api_output_a=generate_1,
            generate_api_output_b=generate_2,
            model="gpt-4.1-mini"  # You can specify a different model if needed
        )
        
        print(f"Received response from compareFromGenerate")
        
        # Convert the response to a serializable dictionary if it's an object
        if hasattr(response, '__dict__'):
            response_dict = vars(response)
        else:
            response_dict = response
            
        # Save the response as a new fixture
        fixture_path = os.path.join(FIXTURE_DIR, 'compare_from_generate.json')
        save_fixture(response_dict, 'compare_from_generate.json')
        print(f"Successfully created fixture: {fixture_path}")
        
    except Exception as e:
        print(f"Error calling compareFromGenerate: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 