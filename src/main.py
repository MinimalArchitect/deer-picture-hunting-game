#!/usr/bin/env python3
"""
Deer Picture Hunting Game - Main Entry Point
"""
from core.game import DeerHuntingGame


def main():
    """Main function to start the game"""
    game = DeerHuntingGame()
    game.run()


if __name__ == "__main__":
    main()
