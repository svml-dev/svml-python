#!/usr/bin/env python
import json
import os
import sys
import re
from svml.client import SVMLClient

# Setup paths
FIXTURE_DIR = os.path.join(os.path.dirname(__file__), 'test-svml', 'fixtures')

PROMPT = """
    In the modern workplace, collaboration between teams is essential for innovation, yet communication barriers often arise due to differing priorities, technical jargon, and organizational silos. 
    While leadership may emphasize agility and rapid iteration, compliance departments focus on risk mitigation and regulatory adherence, sometimes creating friction. 
    Meanwhile, the rise of remote work has introduced both flexibility and new challenges in maintaining team cohesion and knowledge transfer. 
    Informal networks and mentorship programs can bridge some gaps, but not all employees have equal access to these resources. 
    The interplay between technology adoption, employee well-being, and business outcomes is complex: new tools can boost productivity but also cause cognitive overload or resistance to change. 
    Ultimately, the success of an organization depends on its ability to harmonize these diverse elements, foster psychological safety, and adapt to evolving market demands.
"""


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
                    value = re.sub(r'^(["\'])|(["\'])$', '', value)
                    os.environ[key] = value
        return True
    except FileNotFoundError:
        print(f"Warning: Environment file {filename} not found.")
        return False

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
    
    # Initialize the client with API key from environment
    client = SVMLClient(api_key=api_key)
    print(f"Initialized SVMLClient with API key")
    client.authenticate()

    # Prepare request
    request = {
        "context": PROMPT,
        "svml_version": "1.2.2"
    }

    try:
        print("Calling generate for model: gpt-4.1 ...")
        response1 = client.generate(context=PROMPT, svml_version="1.2.2", model="gpt-4.1")
        if hasattr(response1, '__dict__'):
            response1 = vars(response1)
        save_fixture(response1, 'generate_1.json')
        print("Saved generate_1.json")

        print("Calling generate for model: claude-3-5-sonnet-20241022 ...")
        response2 = client.generate(context=PROMPT, svml_version="1.2.2", model="claude-3-5-sonnet-20241022")
        if hasattr(response2, '__dict__'):
            response2 = vars(response2)
        save_fixture(response2, 'generate_2.json')
        print("Saved generate_2.json")

    except Exception as e:
        print(f"Error calling generate: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 