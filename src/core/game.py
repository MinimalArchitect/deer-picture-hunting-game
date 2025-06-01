import json
import os
import random
import time

import pygame

from src.core.game_map import GameMap, GridType
from src.entity.deer import Deer
from src.entity.player import Player, Direction
from src.ui.button import Button
from src.ui.menu import Menu, MenuType
from src.util.color import Color
from src.util.config import WINDOW_WIDTH, GRID_WIDTH, GRID_HEIGHT, WINDOW_HEIGHT
from src.util.sound import Sound
from src.util.texture import Texture

from src.util.score_manager import ScoreManager
from src.ui.name_input_dialog import NameInputDialog


class GameState:
    """Enum for game states"""
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"


class Game:
    """Main game class"""

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Deer Picture Hunting")
        self.clock = pygame.time.Clock()
        self.game_state = GameState.MENU

        # Load textures and sounds
        Texture.load_all()
        Sound.load_all()

        self.sound_enabled = True

        # Create menu
        self.menu = Menu(self.screen)

        # Game objects will be initialized when starting the game
        self.map = None
        self.player = None
        self.deer = []
        self.score = 0
        self.time_left = 60
        self.last_time = time.time()
        self.level_scores = {}  # {level_number: highest_score}
        self.level = 1  # default level selection
        self.score_file = "level_scores.json"
        self.load_scores()

        self.game_active = True
        self.quit_game = False

        self.score_manager = ScoreManager()
        self.name_dialog = None
        self.game_start_time = 0

    def initialize_game(self):
        """Set up the game objects when starting a new game"""
        # Create game objects
        self.map = GameMap()
        self.map.generate_predefined_map(level=self.level)

        # Place player in an empty cell
        self.player = self.place_hunter_in_empty_cell(Color.LIGHT_GREEN)

        # Create deer
        self.deer = []
        for _ in range(10):  # 10 deer
            self.deer.append(self.place_in_empty_cell(Deer))

        # Game state
        self.score = 0
        self.time_left = 60  # 60 seconds
        self.last_time = time.time()
        self.game_state = GameState.PLAYING

        self.game_start_time = time.time()

    def place_in_empty_cell(self, object_class):
        """Place a new object in a random empty cell"""
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)

            if self.map.get_cell(x, y) == GridType.EMPTY:
                return object_class(x, y)

    def place_hunter_in_empty_cell(self, clothes_color):
        """Place a new object in a random empty cell"""
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)

            if self.map.get_cell(x, y) == GridType.EMPTY:
                return Player(x, y, clothes_color)

    def save_scores(self):
        try:
            with open(self.score_file, "w") as f:
                # Ensure keys are strings for JSON compatibility
                json.dump({str(k): v for k, v in self.level_scores.items()}, f)
        except Exception as e:
            print("Error saving scores:", e)

    def load_scores(self):
        if os.path.exists(self.score_file):
            try:
                with open(self.score_file, "r") as f:
                    self.level_scores = json.load(f)
            except Exception as e:
                print("Error loading scores:", e)

    def handle_events(self):
        """Handle pygame events"""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.take_photo()
                elif event.key == pygame.K_ESCAPE:
                    if self.game_state == GameState.PLAYING:
                        self.game_state = GameState.PAUSED
                        self.game_active = False

        has_moved = False

        keys = pygame.key.get_pressed()
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

        if has_moved and self.sound_enabled:
            Sound.move.play()

    def handle_pause_state(self):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))  # Semi-transparent black

        # Create pause menu buttons
        button_width = 200
        button_height = 50
        center_x = WINDOW_WIDTH // 2 - button_width // 2

        continue_btn = (
            Button(center_x, 200, button_width, button_height, "Continue", Color.BUTTON, Color.BUTTON_HOVER))
        main_menu_btn = (
            Button(center_x, 270, button_width, button_height, "Main Menu", Color.BUTTON, Color.BUTTON_HOVER))
        exit_btn = (
            Button(center_x, 340, button_width, button_height, "Exit", Color.BUTTON, Color.BUTTON_HOVER))

        while self.game_state == GameState.PAUSED and not self.quit_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_state = GameState.PLAYING
                        self.game_active = True
                        self.last_time = time.time()
                        return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if continue_btn.is_clicked(mouse_pos, True):
                        self.game_state = GameState.PLAYING
                        self.game_active = True
                        self.last_time = time.time()
                        return
                    elif main_menu_btn.is_clicked(mouse_pos, True):
                        self.game_state = GameState.MENU
                        return
                    elif exit_btn.is_clicked(mouse_pos, True):
                        self.quit_game = True
                        return

            # Draw game
            self.screen.fill(Color.WHITE)
            self.map.draw(self.screen)
            for deer in self.deer:
                deer.draw(self.screen)
            self.player.draw(self.screen)

            # Draw static UI
            font = pygame.font.SysFont(None, 36)
            score_text = font.render(f"Score: {self.score}", True, Color.BLACK)
            time_text = font.render(f"Time: {int(self.time_left)}s", True, Color.BLACK)
            self.screen.blit(score_text, (10, 10))
            self.screen.blit(time_text, (WINDOW_WIDTH - 150, 10))

            # Overlay and pause buttons
            self.screen.blit(overlay, (0, 0))
            for btn in [continue_btn, main_menu_btn, exit_btn]:
                hovered = btn.check_hover(pygame.mouse.get_pos())
                btn.draw(self.screen, hovered)

            pygame.display.flip()
            self.clock.tick(30)

    def take_photo(self):
        """Player takes a photo"""
        if self.sound_enabled:
            Sound.take_photo.play()

        photographed_deer = self.player.take_photo(self.map, self.deer)
        for deer in photographed_deer:
            if not deer.photographed:
                deer.photographed = True
                self.score += 1

    def update(self):
        """Update game state"""
        # Update timer
        current_time = time.time()
        elapsed = current_time - self.last_time
        self.last_time = current_time

        self.time_left -= elapsed
        if self.time_left <= 0:
            self.game_active = False
            self.game_state = GameState.GAME_OVER

        # Update deer
        for deer in self.deer:
            deer.update(self.player, self.map, self.deer)

    def draw(self):
        """Draw everything to the screen"""
        # Clear screen
        self.screen.fill(Color.WHITE)

        # Draw map
        self.map.draw(self.screen)

        # Draw deer
        for deer in self.deer:
            deer.draw(self.screen)

        # Draw player
        self.player.draw(self.screen)

        # Draw UI
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {self.score}", True, Color.BLACK)
        time_text = font.render(f"Time: {int(self.time_left)}s", True, Color.BLACK)

        self.screen.blit(score_text, (10, 10))
        self.screen.blit(time_text, (WINDOW_WIDTH - 150, 10))

        # Update display
        pygame.display.flip()

    def run(self):
        """Main game loop"""
        while not self.quit_game:
            match self.game_state:
                case GameState.MENU:
                    self.handle_menu_state()
                case GameState.PLAYING:
                    self.handle_playing_state()
                case GameState.PAUSED:
                    self.handle_pause_state()
                case GameState.GAME_OVER:
                    self.handle_game_over_state()

        # Quit pygame
        pygame.quit()

    def handle_menu_state(self):
        # Clear event queue before entering menu
        pygame.event.clear()

        # Run menu
        menu_choice = None
        menu_active = True
        while menu_active and not self.quit_game:
            # Process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game = True

                # Handle menu selection based on current menu
                if self.menu.current_menu == MenuType.HIGH_SCORES:
                    # Handle high score screen events
                    if hasattr(self.menu, 'high_score_screen'):
                        result = self.menu.high_score_screen.handle_event(event)
                        if result == "back":
                            self.menu.current_menu = MenuType.MAIN
                            # Clean up the high score screen
                            if hasattr(self.menu, 'high_score_screen'):
                                delattr(self.menu, 'high_score_screen')
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    # Check button clicks only for main menu
                    if self.menu.current_menu == MenuType.MAIN:
                        for i, button in enumerate(self.menu.main_buttons):
                            if button.is_clicked(mouse_pos, True):
                                if i == 0:  # Single Player
                                    menu_choice = "single_player"
                                    menu_active = False
                                elif i == 1:  # Host Game
                                    menu_choice = "host_game"
                                    menu_active = False
                                elif i == 2:  # Join Game
                                    menu_choice = "join_game"
                                    menu_active = False
                                elif i == 3:  # Options
                                    self.menu.current_menu = MenuType.OPTIONS
                                elif i == 4:  # High Scores
                                    self.menu.current_menu = MenuType.HIGH_SCORES
                                elif i == 5:  # Exit
                                    self.quit_game = True

            # Draw menu
            if not self.quit_game:
                self.screen.fill(Color.BACKGROUND)

                if self.menu.current_menu == MenuType.MAIN:
                    # Draw title
                    title_text = self.menu.title_font.render("Deer Picture Hunting", True, Color.BLACK)
                    title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 80))
                    self.screen.blit(title_text, title_rect)

                    # Draw version text
                    version_font = pygame.font.SysFont(None, 24)
                    version_text = version_font.render("2D Grid-Based Version", True, Color.BLACK)
                    version_rect = version_text.get_rect(center=(WINDOW_WIDTH // 2, 120))
                    self.screen.blit(version_text, version_rect)

                    # Draw buttons
                    for button in self.menu.main_buttons:
                        is_hovered = button.check_hover(pygame.mouse.get_pos())
                        button.draw(self.screen, is_hovered)
                        
                elif self.menu.current_menu == MenuType.OPTIONS:
                    result = self.menu.draw_options(self.sound_enabled)
                    if result == "toggle_sound":
                        self.sound_enabled = not self.sound_enabled
                        pygame.time.wait(200)  # Prevent double click
                        
                elif self.menu.current_menu == MenuType.HIGH_SCORES:
                    self.menu.draw_high_scores()

                pygame.display.flip()

            # Control frame rate
            self.clock.tick(30)
            
        # Handle menu choice
        if menu_choice in ["single_player", "host_game", "join_game"]:
            self.handle_level_selection()

    def handle_playing_state(self):
        # Game loop
        self.game_active = True
        while self.game_active and not self.quit_game:
            # Process events
            self.handle_events()

            if not self.game_active:
                continue

            self.update()

            # Draw everything
            self.screen.fill(Color.WHITE)
            self.map.draw(self.screen)
            for deer in self.deer:
                deer.draw(self.screen)
            self.player.draw(self.screen)

            # Draw UI
            font = pygame.font.SysFont(None, 36)
            score_text = font.render(f"Score: {self.score}", True, Color.BLACK)
            time_text = font.render(f"Time: {int(self.time_left)}s", True, Color.BLACK)
            self.screen.blit(score_text, (10, 10))
            self.screen.blit(time_text, (WINDOW_WIDTH - 150, 10))

            pygame.display.flip()
            self.clock.tick(10)

    def handle_level_complete_state(self):
        # Save to old system too for backward compatibility
        if self.score > 0:
            level_key = str(self.level)
            self.level_scores[level_key] = max(self.score, self.level_scores.get(level_key, 0))
            self.save_scores()

        continue_btn = Button(WINDOW_WIDTH // 2 - 100, 260, 200, 50, "Next Level", Color.BUTTON, Color.BUTTON_HOVER)
        menu_btn = Button(WINDOW_WIDTH // 2 - 100, 330, 200, 50, "Main Menu", Color.BUTTON, Color.BUTTON_HOVER)

        while not self.quit_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if continue_btn.is_clicked(mouse_pos, True):
                        if self.level < 20:  # Don't go beyond level 20
                            self.level += 1
                            self.initialize_game()
                            self.game_state = GameState.PLAYING
                            return
                        else:
                            # Completed all levels, go to menu
                            self.game_state = GameState.MENU
                            return
                    elif menu_btn.is_clicked(mouse_pos, True):
                        self.game_state = GameState.MENU
                        return

            self.screen.fill(Color.WHITE)
            font = pygame.font.SysFont(None, 48)
            complete_text = font.render(f"Level {self.level} Complete!", True, Color.BLACK)
            score_text = font.render(f"Score: {self.score}", True, Color.BLACK)
            
            # Show if it was a high score
            record = self.score_manager.get_level_record(self.level)
            if record and record.score == self.score:
                record_text = font.render("NEW RECORD!", True, Color.GREEN)
                self.screen.blit(record_text, (WINDOW_WIDTH // 2 - 120, 120))
            
            self.screen.blit(complete_text, (WINDOW_WIDTH // 2 - 180, 150))
            self.screen.blit(score_text, (WINDOW_WIDTH // 2 - 100, 200))

            for btn in [continue_btn, menu_btn]:
                btn.draw(self.screen, btn.check_hover(pygame.mouse.get_pos()))

            pygame.display.flip()
            self.clock.tick(30)

    def handle_game_over_state(self):
        any_photographed = any(deer.photographed for deer in self.deer)
        
        if any_photographed:
            # Level completed with some deer photographed
            if self.score > 0:
                # Calculate time ONCE at the beginning
                time_taken = time.time() - self.game_start_time
                
                # Check if it's a high score and we haven't shown dialog yet
                if self.score_manager.is_high_score(self.level, self.score) and self.name_dialog is None:
                    print(f"Game completed. Score: {self.score}, Time: {time_taken:.2f}s")
                    print("This is a high score! Showing name dialog...")
                    
                    # Store the time in an instance variable so we don't recalculate
                    self.final_time = time_taken
                    
                    # Initialize name dialog
                    self.name_dialog = NameInputDialog(self.screen, 
                                                    self.score_manager.get_player_name())
                    return  # Exit here to let the dialog run
                
                # If dialog exists and is active, handle it
                if self.name_dialog and self.name_dialog.active:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.quit_game = True
                            return
                        self.name_dialog.handle_event(event)
                    
                    self.name_dialog.update(self.clock.get_time())
                    self.name_dialog.draw()
                    pygame.display.flip()
                    self.clock.tick(30)
                    return  # Stay in this state while dialog is active
                
                # Dialog completed or not needed
                if self.name_dialog and not self.name_dialog.active:
                    print(f"Dialog closed. Result: {self.name_dialog.result}")
                    
                    # Use the stored time, not a new calculation
                    final_time = getattr(self, 'final_time', time_taken)
                    
                    if self.name_dialog.result and self.name_dialog.result.strip():
                        # Player entered a name
                        player_name = self.name_dialog.result.strip()
                        print(f"Dialog result: '{player_name}'")
                        print(f"About to save score: Level={self.level}, Score={self.score}, Time={final_time:.2f}, Player={player_name}")
                        self.score_manager.add_score(self.level, self.score, final_time, player_name)
                    else:
                        # Player cancelled or entered empty name
                        print("No valid name entered, using default")
                        self.score_manager.add_score(self.level, self.score, final_time, "Player")
                    
                    self.name_dialog = None
                    # Clear the stored time
                    if hasattr(self, 'final_time'):
                        delattr(self, 'final_time')
                        
                elif not self.score_manager.is_high_score(self.level, self.score):
                    # Not a high score, save with current player name
                    print("Not a high score, saving normally")
                    self.score_manager.add_score(self.level, self.score, time_taken)
            
            # Move to level complete state
            print("Moving to level complete state")
            self.game_state = GameState.PLAYING  # Temporary state change
            self._show_level_complete()
        else:
            # No deer photographed - game over
            print("No deer photographed, showing game over")
            self.game_state = GameState.PLAYING  # Temporary state change
            self._show_game_over_screen()

    def _show_level_complete(self):
        """Show level complete screen"""
        # DON'T save to old system anymore - it overwrites ScoreManager data
        # if self.score > 0:
        #     level_key = str(self.level)
        #     self.level_scores[level_key] = max(self.score, self.level_scores.get(level_key, 0))
        #     self.save_scores()

        continue_btn = Button(WINDOW_WIDTH // 2 - 100, 260, 200, 50, "Next Level", Color.BUTTON, Color.BUTTON_HOVER)
        menu_btn = Button(WINDOW_WIDTH // 2 - 100, 330, 200, 50, "Main Menu", Color.BUTTON, Color.BUTTON_HOVER)

        level_complete_active = True
        while level_complete_active and not self.quit_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game = True
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if continue_btn.is_clicked(mouse_pos, True):
                        if self.level < 20:  # Don't go beyond level 20
                            self.level += 1
                            self.initialize_game()
                            return  # Exit this method
                        else:
                            # Completed all levels, go to menu
                            self.game_state = GameState.MENU
                            return
                    elif menu_btn.is_clicked(mouse_pos, True):
                        self.game_state = GameState.MENU
                        return

            self.screen.fill(Color.WHITE)
            font = pygame.font.SysFont(None, 48)
            complete_text = font.render(f"Level {self.level} Complete!", True, Color.BLACK)
            score_text = font.render(f"Score: {self.score}", True, Color.BLACK)
            
            # Show if it was a high score
            record = self.score_manager.get_level_record(self.level)
            if record and record.score == self.score and record.player_name != "Legacy Player":
                record_text = font.render("NEW RECORD!", True, Color.GREEN)
                self.screen.blit(record_text, (WINDOW_WIDTH // 2 - 120, 120))
            
            self.screen.blit(complete_text, (WINDOW_WIDTH // 2 - 180, 150))
            self.screen.blit(score_text, (WINDOW_WIDTH // 2 - 100, 200))

            for btn in [continue_btn, menu_btn]:
                btn.draw(self.screen, btn.check_hover(pygame.mouse.get_pos()))

            pygame.display.flip()
            self.clock.tick(30)

    def _show_game_over_screen(self):
        """Show game over screen for when no deer were photographed"""
        game_over_active = True
        pygame.event.clear()
        
        while game_over_active and not self.quit_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game = True
                    return
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    game_over_active = False
                    self.game_state = GameState.MENU
                    return

            self.screen.fill(Color.WHITE)
            font = pygame.font.SysFont(None, 72)
            game_over_text = font.render("GAME OVER", True, Color.BLACK)
            final_score = font.render(f"Final Score: {self.score}", True, Color.BLACK)
            instructions_font = pygame.font.SysFont(None, 32)
            instructions = instructions_font.render("Press any key to continue", True, Color.BLACK)

            self.screen.blit(game_over_text, (WINDOW_WIDTH // 2 - 200, WINDOW_HEIGHT // 2 - 50))
            self.screen.blit(final_score, (WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2 + 20))
            self.screen.blit(instructions, (WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2 + 80))

            pygame.display.flip()
            self.clock.tick(30)

    def handle_level_selection(self):
        pygame.event.clear()
        level_buttons = []
        columns = 5
        spacing = 10
        button_width = 100
        button_height = 40
        start_x = 100
        start_y = 180
        total_levels = 20

        back_btn = Button(WINDOW_WIDTH // 2 - 60, start_y + ((total_levels // columns) + 2) * (button_height + spacing),
                          120, 40, "Back", Color.BUTTON, Color.BUTTON_HOVER)

        for i in range(total_levels):
            row = i // columns
            col = i % columns
            x = start_x + col * (button_width + spacing)
            y = start_y + row * (button_height + spacing)
            level_key = str(i + 1)
            score = self.level_scores.get(level_key, None)
            label = f"{i + 1}" 
            btn_color = Color.BUTTON_DONE if score is not None else Color.BUTTON
            btn_hover = Color.BUTTON_HOVER
            level_buttons.append(Button(x, y, button_width, button_height, label, btn_color, btn_hover))

        selecting = True
        while selecting and not self.quit_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if back_btn.is_clicked(mouse_pos, True):
                        self.game_state = GameState.MENU
                        return
                    for i, btn in enumerate(level_buttons):
                        if btn.is_clicked(mouse_pos, True):
                            self.level = i + 1
                            self.initialize_game()
                            self.game_state = GameState.PLAYING
                            return

            self.screen.fill(Color.BACKGROUND)
            title_font = pygame.font.SysFont(None, 64)
            title_text = title_font.render("Choose Level", True, Color.BLACK)
            self.screen.blit(title_text, (WINDOW_WIDTH // 2 - 180, 100))

            for btn in level_buttons:
                btn.draw(self.screen, btn.check_hover(pygame.mouse.get_pos()))

            back_btn.draw(self.screen, back_btn.check_hover(pygame.mouse.get_pos()))

            pygame.display.flip()
            self.clock.tick(30)