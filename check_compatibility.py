#!/usr/bin/env python3
"""
Compatibility check script for Panda Escape Adventure
This script checks if your system is compatible with the game requirements.
"""

import sys
import os
import platform
import subprocess
import importlib.util

def check_python_version():
    """Check Python version"""
    print("\n=== Python Version Check ===")
    print(f"Python version: {platform.python_version()}")
    print(f"Python implementation: {platform.python_implementation()}")
    print(f"Python executable: {sys.executable}")
    
    # Check if Python version is compatible
    major, minor, _ = platform.python_version_tuple()
    if int(major) != 3 or int(minor) < 8:
        print("WARNING: Python 3.8+ is required. You may experience issues.")
    else:
        print("Python version is compatible.")
    
    # Check for Python 3.13 specifically
    if int(major) == 3 and int(minor) == 13:
        print("You are using Python 3.13. This is a new version and may have compatibility issues.")
        print("If you encounter problems, consider using Python 3.8-3.12 instead.")

def check_environment_variables():
    """Check environment variables"""
    print("\n=== Environment Variables Check ===")
    problematic_vars = ['PYTHONHOME', 'PYTHONPATH']
    for var in problematic_vars:
        if var in os.environ:
            print(f"WARNING: {var} is set to: {os.environ[var]}")
            print(f"This may cause issues. Consider unsetting {var} before running the game.")
        else:
            print(f"{var} is not set. Good!")
    
    print("\nPython path:")
    for path in sys.path:
        print(f"  - {path}")

def check_dependencies():
    """Check if required dependencies are installed"""
    print("\n=== Dependencies Check ===")
    dependencies = ['pygame', 'dotenv']
    
    for dep in dependencies:
        spec = importlib.util.find_spec(dep)
        if spec is None:
            if dep == 'dotenv':
                dep = 'python-dotenv'  # The package name is different from the import name
            print(f"WARNING: {dep} is not installed.")
            print(f"Install it with: pip install {dep}")
        else:
            if dep == 'dotenv':
                dep = 'python-dotenv'
            try:
                # Try to get the version
                if dep == 'python-dotenv':
                    import dotenv
                    version = dotenv.__version__
                elif dep == 'pygame':
                    import pygame
                    version = pygame.version.ver
                print(f"{dep} is installed (version: {version}).")
            except (ImportError, AttributeError):
                print(f"{dep} is installed, but version could not be determined.")

def check_poetry():
    """Check if Poetry is installed and working"""
    print("\n=== Poetry Check ===")
    try:
        result = subprocess.run(['poetry', '--version'], 
                               capture_output=True, 
                               text=True, 
                               check=False)
        if result.returncode == 0:
            print(f"Poetry is installed: {result.stdout.strip()}")
        else:
            print("Poetry seems to be installed but returned an error:")
            print(result.stderr)
    except FileNotFoundError:
        print("Poetry is not installed or not in PATH.")
        print("Install it with: curl -sSL https://install.python-poetry.org | python3 -")

def check_pygame():
    """Check if Pygame is working correctly"""
    print("\n=== Pygame Check ===")
    try:
        import pygame
        pygame.init()
        print(f"Pygame version: {pygame.version.ver}")
        print(f"Pygame modules initialized: {pygame.get_init()}")
        
        # Try to create a simple display
        try:
            screen = pygame.display.set_mode((100, 100))
            pygame.display.set_caption("Test")
            print("Successfully created a Pygame display.")
            pygame.quit()
        except pygame.error as e:
            print(f"WARNING: Could not create Pygame display: {e}")
            print("This might indicate issues with your display server or graphics drivers.")
    except ImportError:
        print("Pygame is not installed.")
    except Exception as e:
        print(f"Error initializing Pygame: {e}")

def main():
    """Run all checks"""
    print("=== Panda Escape Adventure Compatibility Check ===")
    print("This script will check if your system is compatible with the game.")
    
    check_python_version()
    check_environment_variables()
    check_dependencies()
    check_poetry()
    check_pygame()
    
    print("\n=== Summary ===")
    print("If you see any WARNING messages above, you may need to address those issues.")
    print("For more help, refer to the README.md file or run the game with DEBUG=True in the .env file.")

if __name__ == "__main__":
    main() 