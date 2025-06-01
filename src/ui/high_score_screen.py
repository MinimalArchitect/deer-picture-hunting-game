import pygame
from typing import List
from src.util.score_manager import ScoreManager, ScoreEntry
from src.ui.button import Button
from src.util.color import Color

class HighScoreScreen:
    """High score display screen"""
    
    def __init__(self, screen, score_manager: ScoreManager):
        self.screen = screen
        self.score_manager = score_manager
        self.font_large = pygame.font.SysFont(None, 48)
        self.font_medium = pygame.font.SysFont(None, 32)
        self.font_small = pygame.font.SysFont(None, 24)
        
        self.current_level = 1
        self.max_level = 20  # Adjust based on your game
        
        # Create navigation buttons
        self.prev_button = Button(50, 500, 100, 40, "Previous", 
                                Color.BUTTON, Color.BUTTON_HOVER)
        self.next_button = Button(170, 500, 100, 40, "Next", 
                                Color.BUTTON, Color.BUTTON_HOVER)
        self.back_button = Button(650, 500, 100, 40, "Back", 
                                Color.BUTTON, Color.BUTTON_HOVER)
        self.all_levels_button = Button(300, 500, 120, 40, "All Levels", 
                                      Color.BUTTON, Color.BUTTON_HOVER)
        
        self.showing_all = False
    
    def handle_event(self, event) -> str:
        """Handle input events"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            if self.prev_button.is_clicked(mouse_pos, True):
                if self.current_level > 1:
                    self.current_level -= 1
                    self.showing_all = False
            
            elif self.next_button.is_clicked(mouse_pos, True):
                if self.current_level < self.max_level:
                    self.current_level += 1
                    self.showing_all = False
            
            elif self.all_levels_button.is_clicked(mouse_pos, True):
                self.showing_all = not self.showing_all
            
            elif self.back_button.is_clicked(mouse_pos, True):
                return "back"
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and self.current_level > 1:
                self.current_level -= 1
                self.showing_all = False
            elif event.key == pygame.K_RIGHT and self.current_level < self.max_level:
                self.current_level += 1
                self.showing_all = False
            elif event.key == pygame.K_ESCAPE:
                return "back"
        
        return ""
    
    def update(self):
        """Update button hover states"""
        mouse_pos = pygame.mouse.get_pos()
        self.prev_button.check_hover(mouse_pos)
        self.next_button.check_hover(mouse_pos)
        self.back_button.check_hover(mouse_pos)
        self.all_levels_button.check_hover(mouse_pos)
    
    def draw(self):
        """Draw the high score screen"""
        self.screen.fill(Color.BACKGROUND)
        
        if self.showing_all:
            self._draw_all_levels()
        else:
            self._draw_single_level()
        
        # Draw navigation buttons
        self.prev_button.draw(self.screen)
        self.next_button.draw(self.screen)
        self.back_button.draw(self.screen)
        self.all_levels_button.draw(self.screen)
        
        # Draw instructions
        instruction_text = self.font_small.render(
            "Use arrow keys or buttons to navigate levels", 
            True, Color.TEXT
        )
        instruction_rect = instruction_text.get_rect(center=(400, 570))
        self.screen.blit(instruction_text, instruction_rect)
    
    def _draw_single_level(self):
        """Draw high scores for a single level"""
        # Title
        title_text = self.font_large.render(f"Level {self.current_level} High Scores", 
                                          True, Color.TEXT)
        title_rect = title_text.get_rect(center=(400, 50))
        self.screen.blit(title_text, title_rect)
        
        # Get scores for current level
        scores = self.score_manager.get_high_scores(self.current_level, 10)
        
        if not scores:
            no_scores_text = self.font_medium.render("No scores yet!", True, Color.TEXT)
            no_scores_rect = no_scores_text.get_rect(center=(400, 250))
            self.screen.blit(no_scores_text, no_scores_rect)
            return
        
        # Draw headers
        headers = ["Rank", "Player", "Score", "Date", "Time"]
        header_x_positions = [100, 200, 350, 450, 600]
        
        for i, header in enumerate(headers):
            header_text = self.font_medium.render(header, True, Color.TEXT)
            self.screen.blit(header_text, (header_x_positions[i], 100))
        
        # Draw separator line
        pygame.draw.line(self.screen, Color.TEXT, (50, 130), (750, 130), 2)
        
        # Draw scores
        for i, score_entry in enumerate(scores):
            y_pos = 150 + i * 30
            
            # Rank
            rank_text = self.font_small.render(f"{i + 1}.", True, Color.TEXT)
            self.screen.blit(rank_text, (100, y_pos))
            
            # Player name (truncate if too long)
            player_name = score_entry.player_name
            if len(player_name) > 12:
                player_name = player_name[:12] + "..."
            player_text = self.font_small.render(player_name, True, Color.TEXT)
            self.screen.blit(player_text, (200, y_pos))
            
            # Score
            score_text = self.font_small.render(str(score_entry.score), True, Color.TEXT)
            self.screen.blit(score_text, (350, y_pos))
            
            # Date (show only date, not time)
            date_str = score_entry.date.split(' ')[0] if score_entry.date else "Unknown"
            date_text = self.font_small.render(date_str, True, Color.TEXT)
            self.screen.blit(date_text, (450, y_pos))
            
            # Time taken
            if hasattr(score_entry, 'time_taken') and score_entry.time_taken > 0:
                time_str = f"{score_entry.time_taken:.1f}s"
            else:
                time_str = "N/A"
            time_text = self.font_small.render(time_str, True, Color.TEXT)
            self.screen.blit(time_text, (600, y_pos))
    
    def _draw_all_levels(self):
        """Draw overview of all levels with record scores"""
        # Title
        title_text = self.font_large.render("All Level Records", True, Color.TEXT)
        title_rect = title_text.get_rect(center=(400, 50))
        self.screen.blit(title_text, title_rect)
        
        # Draw headers
        headers = ["Level", "Record Holder", "Best Score"]
        header_x_positions = [150, 300, 500]
        
        for i, header in enumerate(headers):
            header_text = self.font_medium.render(header, True, Color.TEXT)
            self.screen.blit(header_text, (header_x_positions[i], 100))
        
        # Draw separator line
        pygame.draw.line(self.screen, Color.TEXT, (100, 130), (650, 130), 2)
        
        # Draw level records (show only first 15 levels to fit on screen)
        max_display = 15
        for level in range(1, min(self.max_level + 1, max_display + 1)):
            y_pos = 150 + (level - 1) * 25
            
            # Level number
            level_text = self.font_small.render(f"Level {level}", True, Color.TEXT)
            self.screen.blit(level_text, (150, y_pos))
            
            # Get record for this level
            record = self.score_manager.get_level_record(level)
            
            if record:
                # Record holder name (truncate if needed)
                holder_name = record.player_name
                if len(holder_name) > 15:
                    holder_name = holder_name[:15] + "..."
                holder_text = self.font_small.render(holder_name, True, Color.TEXT)
                self.screen.blit(holder_text, (300, y_pos))
                
                # Best score
                score_text = self.font_small.render(str(record.score), True, Color.TEXT)
                self.screen.blit(score_text, (500, y_pos))
            else:
                # No scores yet
                no_score_text = self.font_small.render("No scores", True, Color.GRAY)
                self.screen.blit(no_score_text, (300, y_pos))