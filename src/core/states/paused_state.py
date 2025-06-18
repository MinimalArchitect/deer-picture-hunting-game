"""
Paused state for the deer hunting game.
Handles the pause menu and game pause functionality.
"""

import pygame
from src.core.game_state import TransitionableState
from src.ui.button import Button
from src.util.color import Color
from src.util.config import WINDOW_WIDTH, WINDOW_HEIGHT


class PausedState(TransitionableState):
    """
    Handles the pause menu including:
    - Continue/resume game
    - Return to main menu
    - Exit game
    - Pause overlay
    """
    
    def __init__(self, game_context):
        super().__init__(game_context)
        
        # Pause menu buttons
        self.continue_btn = None
        self.main_menu_btn = None
        self.exit_btn = None
        
        # Background snapshot for overlay effect
        self.background_surface = None
        self.overlay_surface = None
        
        # Button setup
        self._setup_buttons()
    
    def enter(self, previous_state=None, **kwargs):
        """Initialize pause state."""
        super().enter(previous_state, **kwargs)
        
        # Create background snapshot for overlay effect
        self._create_background_overlay()
        
        # Clear any accumulated events
        pygame.event.clear()
        
        print("Game paused")
    
    def exit(self, next_state=None):
        """Clean up when leaving pause state."""
        super().exit(next_state)
        
        # Clean up surfaces
        self.background_surface = None
        self.overlay_surface = None
        
        print("Game unpaused")
    
    def update(self, dt):
        """Update pause state logic."""
        # Check for transition requests
        transition = self.check_transition()
        if transition:
            return transition
        
        # Update button hover states
        mouse_pos = pygame.mouse.get_pos()
        self.continue_btn.check_hover(mouse_pos)
        self.main_menu_btn.check_hover(mouse_pos)
        self.exit_btn.check_hover(mouse_pos)
        
        return None
    
    def render(self):
        """Render the pause screen."""
        # Draw the background overlay
        if self.background_surface:
            self.screen.blit(self.background_surface, (0, 0))
        
        if self.overlay_surface:
            self.screen.blit(self.overlay_surface, (0, 0))
        
        # Draw pause menu title
        self._render_pause_title()
        
        # Draw pause menu buttons
        self._render_pause_buttons()
        
        # Draw instructions
        self._render_instructions()
        
        # Update display
        pygame.display.flip()
    
    def handle_event(self, event):
        """Handle pause menu events."""
        # Handle quit events
        quit_result = super().handle_event(event)
        if quit_result:
            return quit_result
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Resume game on ESC
                self.request_transition("playing")
                return self.check_transition()
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            return self._handle_mouse_click(event)
        
        return None
    
    def _setup_buttons(self):
        """Set up pause menu buttons."""
        button_width = 200
        button_height = 50
        center_x = WINDOW_WIDTH // 2 - button_width // 2
        
        self.continue_btn = Button(
            center_x, 250, button_width, button_height,
            "Continue", Color.BUTTON, Color.BUTTON_HOVER
        )
        
        self.main_menu_btn = Button(
            center_x, 320, button_width, button_height,
            "Main Menu", Color.BUTTON, Color.BUTTON_HOVER
        )
        
        self.exit_btn = Button(
            center_x, 390, button_width, button_height,
            "Exit Game", Color.BUTTON, Color.BUTTON_HOVER
        )
    
    def _create_background_overlay(self):
        """Create semi-transparent overlay over the game."""
        # Create overlay surface
        self.overlay_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        self.overlay_surface.fill((0, 0, 0, 150))  # Semi-transparent black
    
    def _render_pause_title(self):
        """Render the pause menu title."""
        font = pygame.font.SysFont(None, 72)
        title_text = font.render("PAUSED", True, Color.WHITE)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 180))
        self.screen.blit(title_text, title_rect)
    
    def _render_pause_buttons(self):
        """Render pause menu buttons."""
        mouse_pos = pygame.mouse.get_pos()
        
        # Draw buttons with hover effects
        self.continue_btn.draw(self.screen, self.continue_btn.check_hover(mouse_pos))
        self.main_menu_btn.draw(self.screen, self.main_menu_btn.check_hover(mouse_pos))
        self.exit_btn.draw(self.screen, self.exit_btn.check_hover(mouse_pos))
    
    def _render_instructions(self):
        """Render pause instructions."""
        font = pygame.font.SysFont(None, 32)
        instruction_text = font.render("Press ESC to resume", True, Color.WHITE)
        instruction_rect = instruction_text.get_rect(center=(WINDOW_WIDTH // 2, 460))
        self.screen.blit(instruction_text, instruction_rect)
    
    def _handle_mouse_click(self, event):
        """Handle mouse click events."""
        mouse_pos = pygame.mouse.get_pos()
        
        if self.continue_btn.is_clicked(mouse_pos, True):
            self.request_transition("playing")
            return self.check_transition()
        
        elif self.main_menu_btn.is_clicked(mouse_pos, True):
            # Transition to menu, will lose current game progress
            self.request_transition("menu")
            return self.check_transition()
        
        elif self.exit_btn.is_clicked(mouse_pos, True):
            return "quit"
        
        return None