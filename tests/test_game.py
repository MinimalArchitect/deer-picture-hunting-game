"""
A simple test script to verify the basic game setup works
"""
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.game import DeerHuntingGame

def main():
    """Run a simple test of the game"""
    game = DeerHuntingGame()
    game.run()

if __name__ == "__main__":
    main()