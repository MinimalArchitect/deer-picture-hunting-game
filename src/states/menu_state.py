"""
Menu state for the deer hunting game.
Handles the main menu interface and navigation.
"""

import pygame
from src.core.game_state import TransitionableState
from src.ui.menu import Menu, MenuType
from src.util.color import Color
from src.util.config import WINDOW_WIDTH, WINDOW_HEIGHT


class MenuState(TransitionableState):
    """
    Handles the main menu system including:
    - Main menu navigation
    - Options menu
    - High scores display
    - Menu transitions
    """
    
    def __init__(self, game_context):
        super().__init__(game_context)
        self.menu = None
        self.menu_initialized = False
        
    def enter(self, previous_state=None, **kwargs):
        """Initialize menu when entering state."""
        super().enter(previous_state, **kwargs)
        
        # Initialize menu if not already done
        if not self.menu_initialized:
            self.menu = Menu(self.screen)
            self.menu_initialized = True
        
        # Reset to main menu
        self.menu.current_menu = MenuType.MAIN
        
        # Clear any pygame events that might have accumulated
        pygame.event.clear()
        
        print("Menu state entered")
    
    def exit(self, next_state=None):
        """Clean up when leaving menu state."""
        super().exit(next_state)
        # Menu object is kept for reuse, just cleanup any temporary state
        if hasattr(self.menu, 'high_score_screen'):
            delattr(self.menu, 'high_score_screen')
    
    def update(self, dt):
        """Update menu logic."""
        # Check for any transition requests
        transition = self.check_transition()
        if transition:
            return transition
        
        # No specific update logic needed for menu - it's event-driven
        return None
    
    def render(self):
        """Render the menu interface."""
        # Clear screen with background color
        self.screen.fill(Color.BACKGROUND)
        
        if self.menu.current_menu == MenuType.MAIN:
            self._render_main_menu()
        elif self.menu.current_menu == MenuType.OPTIONS:
            self._render_options_menu()
        elif self.menu.current_menu == MenuType.HIGH_SCORES:
            self._render_high_scores_menu()
        
        # Update display
        pygame.display.flip()
    
    def handle_event(self, event):
        """Handle menu events."""
        # Handle quit events
        quit_result = super().handle_event(event)
        if quit_result:
            return quit_result
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            return self._handle_mouse_click(event)
        
        # Handle high score screen events if active
        if (self.menu.current_menu == MenuType.HIGH_SCORES and 
            hasattr(self.menu, 'high_score_screen')):
            result = self.menu.high_score_screen.handle_event(event)
            if result == "back":
                self.menu.current_menu = MenuType.MAIN
                # Clean up the high score screen
                if hasattr(self.menu, 'high_score_screen'):
                    delattr(self.menu, 'high_score_screen')
        
        return None
    
    def _render_main_menu(self):
        """Render the main menu screen."""
        # Draw title
        title_text = self.menu.title_font.render("Deer Picture Hunting", True, Color.BLACK)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 80))
        self.screen.blit(title_text, title_rect)
        
        # Draw version text
        version_font = pygame.font.SysFont(None, 24)
        version_text = version_font.render("2D Grid-Based Version", True, Color.BLACK)
        version_rect = version_text.get_rect(center=(WINDOW_WIDTH // 2, 120))
        self.screen.blit(version_text, version_rect)
        
        # Draw main menu buttons
        mouse_pos = pygame.mouse.get_pos()
        for button in self.menu.main_buttons:
            is_hovered = button.check_hover(mouse_pos)
            button.draw(self.screen, is_hovered)
    
    def _render_options_menu(self):
        """Render the options menu."""
        result = self.menu.draw_options(self.game.sound_enabled)
        if result == "toggle_sound":
            self.game.sound_enabled = not self.game.sound_enabled
            pygame.time.wait(200)  # Prevent double click
    
    def _render_high_scores_menu(self):
        """Render the high scores menu."""
        self.menu.draw_high_scores()
    
    def _handle_mouse_click(self, event):
        """Handle mouse click events."""
        mouse_pos = pygame.mouse.get_pos()
        
        # Only handle clicks for main menu
        if self.menu.current_menu == MenuType.MAIN:
            for i, button in enumerate(self.menu.main_buttons):
                if button.is_clicked(mouse_pos, True):
                    return self._handle_main_menu_selection(i)
        
        return None
    
    def _handle_main_menu_selection(self, button_index):
        """Handle main menu button selection."""
        if button_index == 0:  # Single Player
            self.request_transition("level_selection", game_mode="single_player")
            return self.check_transition()
        elif button_index == 1:  # Host Game
            self.request_transition("level_selection", game_mode="host_game")
            return self.check_transition()
        elif button_index == 2:  # Join Game
            self.request_transition("level_selection", game_mode="join_game")
            return self.check_transition()
        elif button_index == 3:  # Options
            self.menu.current_menu = MenuType.OPTIONS
        elif button_index == 4:  # High Scores
            self.menu.current_menu = MenuType.HIGH_SCORES
        elif button_index == 5:  # Exit
            return "quit"
        
        return None