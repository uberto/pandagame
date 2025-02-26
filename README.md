# Panda Escape Adventure

A fun platformer game where you play as a panda trying to escape and free your animal friends! Navigate through different islands, climb bamboo, avoid zookeepers, and rescue your caged friends.

## Features
- Play as a cute panda character
- Jump, run, and climb bamboo
- Multiple levels with different island themes
- Rescue caged animal friends
- Avoid zookeepers
- Platformer-style gameplay inspired by Lode Runner
- Scrolling levels that extend beyond the screen
- Island-themed levels with ocean boundaries

## Installation
1. Make sure you have Python 3.8+ installed
2. Install Poetry (dependency management tool):
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```
   or follow the instructions at https://python-poetry.org/docs/#installation

3. Install dependencies:
   ```bash
   poetry install
   ```

## Python 3.13 Compatibility
This game is compatible with Python 3.8 through 3.13. If you're using Python 3.13, which is a newer version, you might encounter some compatibility issues. We've included special handling for Python 3.13 in the run scripts.

To check if your system is compatible, run:
```bash
./check_compatibility.py
```

This script will check your Python version, environment variables, and required dependencies to help diagnose any issues.

## Configuration
The game uses environment variables for configuration, which are loaded from a `.env` file. You can customize these settings by editing the `.env` file:

```
# Game settings
GAME_TITLE=Panda Escape Adventure
WINDOW_WIDTH=800
WINDOW_HEIGHT=600
FPS=60
DEBUG=True
```

## Running the Game

### Using Poetry
```bash
poetry run python main.py
```

### Using the Shell Script (Linux/Mac)
We've included a shell script that automatically unsets problematic environment variables and handles Python 3.13 specifically:

```bash
./run_game.sh
```

If you encounter any issues with Python environment variables (like PYTHONHOME or PYTHONPATH), the script will help ensure a clean environment for running the game.

## Controls
- Arrow Left/Right: Move the panda left and right
- Space: Jump when on the ground
- Up/Down: Climb bamboo (press once to start climbing, release to stop)
- P: Pause/Unpause the game
- Enter: Select menu options

### Climbing Tips
- When touching bamboo, press Up or Down to start climbing
- The panda will continue climbing in that direction until you release the key
- You can still move left and right while climbing
- Platforms won't block your movement while climbing bamboo

### Scrolling Levels
- Each level extends beyond the visible screen
- The camera will automatically follow your panda as you move
- Explore the entire level to find all caged animals
- The screen smoothly scrolls horizontally and vertically as you move
- Each level is an island surrounded by ocean - you can't fall off the edges!
- Beach edges and palm trees mark the boundaries of the island

## Troubleshooting
If you encounter issues with Python paths or environment variables, try:

1. Running the compatibility check script: `./check_compatibility.py`
2. Running the game with the provided shell script: `./run_game.sh`
3. Manually unsetting environment variables:
   ```bash
   unset PYTHONHOME
   unset PYTHONPATH
   poetry run python main.py
   ```
4. Check the debug output by setting `DEBUG=True` in the `.env` file

### Common Issues with Python 3.13
Python 3.13 is a newer version and might have compatibility issues with some libraries. If you encounter problems:

1. Try using an earlier Python version (3.8-3.12) if available
2. Make sure you have the latest version of pygame installed
3. Run with DEBUG=True to see more detailed error messages
4. Check if there are any specific error messages related to Python 3.13