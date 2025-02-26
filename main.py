import os
import sys
import subprocess
import platform

# Print Python version information
print(f"Python version: {platform.python_version()}")
print(f"Python implementation: {platform.python_implementation()}")
print(f"Python executable: {sys.executable}")

# Ensure we're running in the correct directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
print(f"Working directory: {os.getcwd()}")

# Unset problematic environment variables
if 'PYTHONHOME' in os.environ:
    print(f"Unsetting PYTHONHOME environment variable: {os.environ['PYTHONHOME']}")
    del os.environ['PYTHONHOME']
if 'PYTHONPATH' in os.environ:
    print(f"Unsetting PYTHONPATH environment variable: {os.environ['PYTHONPATH']}")
    del os.environ['PYTHONPATH']

# Add the current directory to the Python path
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)
    print(f"Added {script_dir} to Python path")

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("Environment variables loaded from .env file")
except ImportError as e:
    print(f"Error importing python-dotenv: {e}")
    print("python-dotenv not installed. Using default settings.")
    # Set default environment variables
    os.environ.setdefault('GAME_TITLE', 'Panda Escape Adventure')
    os.environ.setdefault('WINDOW_WIDTH', '800')
    os.environ.setdefault('WINDOW_HEIGHT', '600')
    os.environ.setdefault('FPS', '60')
    os.environ.setdefault('DEBUG', 'False')

# Check for pygame
try:
    import pygame
    print(f"Pygame version: {pygame.version.ver}")
except ImportError as e:
    print(f"Error importing pygame: {e}")
    print("Please make sure pygame is installed correctly.")
    print("Try running: poetry install")
    sys.exit(1)

# Import the game after environment setup
try:
    from panda_game.game import Game
    
    if __name__ == "__main__":
        print("Starting Panda Escape Adventure...")
        game = Game()
        game.run()
except ImportError as e:
    print(f"Error importing game modules: {e}")
    print("\nThis might be due to a Python path issue.")
    print("Make sure you're running the game from the correct directory.")
    print("Try running: ./run_game.sh")
    
    # Wait for user input before exiting
    input("\nPress Enter to exit...")
    sys.exit(1)
except Exception as e:
    print(f"Error starting the game: {e}")
    print("\nDebug information:")
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print(f"Python path: {sys.path}")
    print(f"Current directory: {os.getcwd()}")
    
    # Wait for user input before exiting
    input("\nPress Enter to exit...")
    sys.exit(1) 