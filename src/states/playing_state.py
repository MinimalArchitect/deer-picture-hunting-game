"""
Playing state for the deer hunting game.
Handles the main gameplay loop, player controls, and game logic.
"""

import pygame
import time
from src.core.game_state import TransitionableState
from src.core.game_map import GameMap
from src.entity.player import Player, Direction
from src.entity.deer import Deer
from src.util.color import Color
from src.util.config import WINDOW_WIDTH, WINDOW_HEIGHT, GRID_WIDTH, GRID_HEIGHT
from src.util.sound import Sound
import random


class PlayingState(TransitionableState):
    """
    Handles the main gameplay including:
    - Player movement and controls
    - Deer AI and behavior
    - Game timer and scoring
    - Photography mechanics
    """
    
    def __init__(self, game_context):
        super().__init__(game_context)
        
        # Game objects
        self.map = None
        self.player = None
        self.deer = []
        
        # Game state
        self.score = 0
        self.time_left = 60
        self.last_time = 0
        self.game_start_time = 0
        self.level = 1
        
        # Game control
        self.game_active = True
    
    def enter(self, previous_state=None, **kwargs):
        """Initialize the game when entering playing state."""
        super().enter(previous_state, **kwargs)
        
        # Get level from transition data or use current level
        self.level = kwargs.get('level', getattr(self.game, 'level', 1))
        
        # Update the game context with the new level
        self.game.level = self.level
        
        # Initialize the game
        self._initialize_game()
        
        print(f"Playing state entered - Level {self.level}")
    
    def exit(self, next_state=None):
        """Clean up when leaving playing state."""
        super().exit(next_state)
        
        # Store final game data in game context for other states to access
        self.game.score = self.score
        self.game.level = self.level
        self.game.game_start_time = self.game_start_time
        self.game.deer = self.deer  # For game over state to check photographed deer
        
        print("Playing state exited")
    
    def update(self, dt):
        """Update game logic."""
        # Check for transition requests first
        transition = self.check_transition()
        if transition:
            return transition
        
        if not self.game_active:
            return None
        
        # Update timer
        current_time = time.time()
        elapsed = current_time - self.last_time
        self.last_time = current_time
        
        self.time_left -= elapsed
        
        # Check if time is up
        if self.time_left <= 0:
            self.game_active = False
            self.request_transition("game_over")
            return self.check_transition()
        
        # Update deer
        for deer in self.deer:
            deer.update(self.player, self.map, self.deer)
        
        return None
    
    def render(self):
        """Render the game."""
        # Clear screen
        self.screen.fill(Color.WHITE)
        
        # Draw game objects
        self.map.draw(self.screen)
        
        for deer in self.deer:
            deer.draw(self.screen)
        
        self.player.draw(self.screen)
        
        # Draw UI
        self._render_ui()
        
        # Update display
        pygame.display.flip()
    
    def handle_event(self, event):
        """Handle game events."""
        # Handle quit events
        quit_result = super().handle_event(event)
        if quit_result:
            return quit_result
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self._take_photo()
            elif event.key == pygame.K_ESCAPE:
                self.request_transition("paused")
                return self.check_transition()
        
        # Handle continuous key presses for movement
        self._handle_movement()
        
        return None
    
    def _initialize_game(self):
        """Set up the game objects when starting a new game."""
        # Create game objects
        self.map = GameMap()
        self.map.generate_predefined_map(level=self.level)
        
        # Place player in an empty cell
        self.player = self._place_hunter_in_empty_cell(Color.LIGHT_GREEN)
        
        # Create deer
        self.deer = []
        for _ in range(10):  # 10 deer
            self.deer.append(self._place_in_empty_cell(Deer))
        
        # Initialize game state
        self.score = 0
        self.time_left = 60  # 60 seconds
        self.last_time = time.time()
        self.game_start_time = time.time()
        self.game_active = True
        
        print(f"Game initialized for level {self.level}")
    
    def _place_in_empty_cell(self, object_class):
        """Place a new object in a random empty cell."""
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            
            if self.map.get_cell(x, y) == "EMPTY":
                return object_class(x, y)
    
    def _place_hunter_in_empty_cell(self, clothes_color):
        """Place a hunter in a random empty cell."""
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            
            if self.map.get_cell(x, y) == "EMPTY":
                return Player(x, y, clothes_color)
    
    def _handle_movement(self):
        """Handle continuous movement input."""
        keys = pygame.key.get_pressed()
        has_moved = False
        
        if keys[pygame.K_UP]:
            self.player.direction = Direction.UP
            has_moved = self.player.move(0, -1, self.map, self.deer)
        elif keys[pygame.K_DOWN]:
            self.player.direction = Direction.DOWN
            has_moved = self.player.move(0, 1, self.map, self.deer)
        elif keys[pygame.K_LEFT]:
            self.player.direction = Direction.LEFT
            has_moved = self.player.move(-1, 0, self.map, self.deer)
        elif keys[pygame.K_RIGHT]:
            self.player.direction = Direction.RIGHT
            has_moved = self.player.move(1, 0, self.map, self.deer)
        
        # Play movement sound if moved and sound is enabled
        if has_moved and self.game.sound_enabled:
            Sound.move.play()
    
    def _take_photo(self):
        """Handle photo taking."""
        if self.game.sound_enabled:
            Sound.take_photo.play()
        
        photographed_deer = self.player.take_photo(self.map, self.deer)
        for deer in photographed_deer:
            if not deer.photographed:
                deer.photographed = True
                self.score += 1
                print(f"Deer photographed! Score: {self.score}")
    
    def _render_ui(self):
        """Render the game UI."""
        font = pygame.font.SysFont(None, 36)
        
        # Score text
        score_text = font.render(f"Score: {self.score}", True, Color.BLACK)
        self.screen.blit(score_text, (10, 10))
        
        # Time text
        time_text = font.render(f"Time: {int(self.time_left)}s", True, Color.BLACK)
        self.screen.blit(time_text, (WINDOW_WIDTH - 150, 10))
        
        # Level text
        level_text = font.render(f"Level: {self.level}", True, Color.BLACK)
        self.screen.blit(level_text, (10, 50))