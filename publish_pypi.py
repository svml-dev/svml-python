import os
import shutil
import subprocess
import sys

# --- Configuration ---
# The root directory of the Python package (where pyproject.toml is located)
PACKAGE_ROOT = os.path.dirname(os.path.abspath(__file__))
# The name of the .egg-info directory, which can vary slightly.
# We'll find it dynamically, but common pattern is 'svml.egg-info'
EGG_INFO_DIR_NAME = "svml.egg-info" 

# --- Helper Functions ---
def run_command(command, cwd=None):
    """Runs a shell command and prints its output."""
    print(f"\nExecuting command: {' '.join(command)}")
    try:
        process = subprocess.Popen(command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
        for line in iter(process.stdout.readline, ''):
            print(line, end='')
        process.wait()
        if process.returncode != 0:
            print(f"\nError: Command {' '.join(command)} failed with exit code {process.returncode}")
            sys.exit(process.returncode)
        print(f"Command {' '.join(command)} executed successfully.")
        return True
    except FileNotFoundError:
        print(f"\nError: Command not found. Is '{command[0]}' installed and in your PATH?")
        if command[0] == "twine":
            print("Please install twine: pip install twine")
        elif command[0] == sys.executable and command[1] == "-m" and command[2] == "build":
            print("Please install the build package: pip install build")
        sys.exit(1)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        sys.exit(1)

def remove_if_exists(path):
    """Removes a file or directory if it exists."""
    if os.path.isfile(path) or os.path.islink(path):
        os.unlink(path)
        print(f"Removed file: {path}")
    elif os.path.isdir(path):
        shutil.rmtree(path)
        print(f"Removed directory: {path}")

# --- Main Publishing Steps ---
def main():
    print("Starting PyPI publishing process...")
    os.chdir(PACKAGE_ROOT)
    print(f"Changed working directory to: {PACKAGE_ROOT}")

    # 1. Clean up old build artifacts
    print("\n--- Step 1: Cleaning up old build artifacts ---")
    remove_if_exists(os.path.join(PACKAGE_ROOT, "dist"))
    remove_if_exists(os.path.join(PACKAGE_ROOT, "build"))
    
    # Dynamically find and remove .egg-info directory
    # It's usually in the PACKAGE_ROOT for `python -m build`
    items_in_package_root = os.listdir(PACKAGE_ROOT)
    for item in items_in_package_root:
        if item.endswith(".egg-info"):
            remove_if_exists(os.path.join(PACKAGE_ROOT, item))
            break # Assuming only one relevant .egg-info
    print("Cleanup complete.")

    # 2. Build the package
    print("\n--- Step 2: Building the package ---")
    # Ensure we're using the python executable that's running this script
    python_executable = sys.executable
    if not run_command([python_executable, "-m", "build"], cwd=PACKAGE_ROOT):
        return # Exit if build fails

    # 3. Upload to PyPI
    print("\n--- Step 3: Uploading to PyPI ---")
    print("Twine will now attempt to upload. You might be prompted for your PyPI credentials.")
    if not run_command(["twine", "upload", "dist/*"], cwd=PACKAGE_ROOT):
        return # Exit if upload fails
        
    print("\n-------------------------------------")
    print("PyPI publishing process completed successfully!")
    print("Please verify the new version on PyPI.")
    print("-------------------------------------")

if __name__ == "__main__":
    main()
