import pygame
from src.util.color import Color
from src.ui.button import Button

class NameInputDialog:
    """Dialog for entering player name"""
    
    def __init__(self, screen, initial_name: str = ""):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 32)
        self.input_text = initial_name
        self.cursor_visible = True
        self.cursor_timer = 0
        self.active = True
        self.result = None
        
        # Create buttons
        self.ok_button = Button(280, 350, 80, 40, "OK", 
                              Color.BUTTON, Color.BUTTON_HOVER)
        self.cancel_button = Button(380, 350, 80, 40, "Cancel", 
                                  Color.BUTTON, Color.BUTTON_HOVER)
        
        # Dialog dimensions
        self.dialog_rect = pygame.Rect(200, 200, 400, 250)
    
    def handle_event(self, event):
        """Handle input events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.result = self.input_text.strip() or "Player"
                self.active = False
            elif event.key == pygame.K_ESCAPE:
                self.result = None
                self.active = False
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            else:
                # Add character if it's printable and not too long
                if event.unicode.isprintable() and len(self.input_text) < 20:
                    self.input_text += event.unicode
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            if self.ok_button.is_clicked(mouse_pos, True):
                self.result = self.input_text.strip() or "Player"
                self.active = False
            elif self.cancel_button.is_clicked(mouse_pos, True):
                self.result = None
                self.active = False
    
    def update(self, dt):
        """Update dialog state"""
        # Update cursor blinking
        self.cursor_timer += dt
        if self.cursor_timer >= 500:  # Blink every 500ms
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0
        
        # Update button hover states
        mouse_pos = pygame.mouse.get_pos()
        self.ok_button.check_hover(mouse_pos)
        self.cancel_button.check_hover(mouse_pos)
    
    def draw(self):
        """Draw the name input dialog"""
        # Draw semi-transparent overlay
        overlay = pygame.Surface(self.screen.get_size())
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Draw dialog background
        pygame.draw.rect(self.screen, Color.DIALOG_BG, self.dialog_rect)
        pygame.draw.rect(self.screen, Color.TEXT, self.dialog_rect, 3)
        
        # Draw title
        title_text = self.font.render("Enter Your Name", True, Color.TEXT)
        title_rect = title_text.get_rect(center=(self.dialog_rect.centerx, 
                                                self.dialog_rect.top + 40))
        self.screen.blit(title_text, title_rect)
        
        # Draw input box
        input_rect = pygame.Rect(self.dialog_rect.centerx - 150, 
                               self.dialog_rect.centery - 20, 300, 40)
        pygame.draw.rect(self.screen, Color.WHITE, input_rect)
        pygame.draw.rect(self.screen, Color.TEXT, input_rect, 2)
        
        # Draw input text
        display_text = self.input_text
        if self.cursor_visible:
            display_text += "|"
        
        text_surface = self.font.render(display_text, True, Color.BLACK)
        text_rect = text_surface.get_rect()
        text_rect.left = input_rect.left + 10
        text_rect.centery = input_rect.centery
        
        # Clip text if it's too long
        if text_rect.width > input_rect.width - 20:
            # Show only the end of the text
            text_surface = self.font.render("..." + display_text[-15:], True, Color.BLACK)
            text_rect = text_surface.get_rect()
            text_rect.left = input_rect.left + 10
            text_rect.centery = input_rect.centery
        
        self.screen.blit(text_surface, text_rect)
        
        # Draw buttons
        self.ok_button.draw(self.screen)
        self.cancel_button.draw(self.screen)
        
        # Draw instructions
        instruction_text = pygame.font.SysFont(None, 24).render(
            "Press Enter to confirm, Escape to cancel", True, Color.TEXT
        )
        instruction_rect = instruction_text.get_rect(
            center=(self.dialog_rect.centerx, self.dialog_rect.bottom - 30)
        )
        self.screen.blit(instruction_text, instruction_rect)