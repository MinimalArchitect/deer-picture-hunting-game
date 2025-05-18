import random
import time

import pygame

from src.core.game_map import GameMap, GridType
from src.entity.deer import Deer
from src.entity.player import Player, Direction
from src.ui.menu import Menu, MenuType
from src.util.color import Color
from src.util.config import WINDOW_WIDTH, GRID_WIDTH, GRID_HEIGHT, WINDOW_HEIGHT
from src.util.texture import Texture


class GameState:
    """Enum for game states"""
    MENU = "menu"
    PLAYING = "playing"
    GAME_OVER = "game_over"


class Game:
    """Main game class"""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Deer Picture Hunting")
        self.clock = pygame.time.Clock()
        self.game_state = GameState.MENU

        Texture.load_all()

        # Create menu
        self.menu = Menu(self.screen)

        # Game objects will be initialized when starting the game
        self.map = None
        self.player = None
        self.deer = []
        self.score = 0
        self.time_left = 60
        self.last_time = time.time()

        self.quit_game = False

    def initialize_game(self):
        """Set up the game objects when starting a new game"""
        # Create game objects
        self.map = GameMap()
        self.map.generate_map()

        # Place player in an empty cell
        self.player = self.place_in_empty_cell(Player)

        # Create deer
        self.deer = []
        for _ in range(10):  # 10 deer
            self.deer.append(self.place_in_empty_cell(Deer))

        # Game state
        self.score = 0
        self.time_left = 60  # 60 seconds
        self.last_time = time.time()
        self.game_state = GameState.PLAYING

    def place_in_empty_cell(self, object_class):
        """Place a new object in a random empty cell"""
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)

            if self.map.get_cell(x, y) == GridType.EMPTY:
                return object_class(x, y)

    def handle_events(self):
        """Handle pygame events"""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.take_photo()
                elif event.key == pygame.K_ESCAPE:
                    # Return to menu on escape
                    self.game_active = False
                    self.game_state = GameState.MENU

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.player.direction = Direction.UP
            self.player.move(0, -1, self.map)
        elif keys[pygame.K_DOWN]:
            self.player.direction = Direction.DOWN
            self.player.move(0, 1, self.map)
        elif keys[pygame.K_LEFT]:
            self.player.direction = Direction.LEFT
            self.player.move(-1, 0, self.map)
        elif keys[pygame.K_RIGHT]:
            self.player.direction = Direction.RIGHT
            self.player.move(1, 0, self.map)

    def take_photo(self):
        """Player takes a photo"""
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
            deer.update(self.player, self.map)

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

                # Handle menu selection
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    # Check button clicks
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
                                self.menu.current_menu = "options"
                            elif i == 4:  # High Scores
                                self.menu.current_menu = "high_scores"
                            elif i == 5:  # Exit
                                self.quit_game = True

            # Draw menu
            if not self.quit_game:
                self.screen.fill(self.menu.bg_color)

                # Draw title
                title_text = self.menu.title_font.render("Deer Picture Hunting", True, Color.BLACK)
                title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 80))
                self.screen.blit(title_text, title_rect)

                # Draw version text
                version_font = pygame.font.SysFont(None, 24)
                version_text = version_font.render("2D Grid-Based Version", True, Color.BLACK)
                version_rect = version_text.get_rect(center=(WINDOW_WIDTH // 2, 120))
                self.screen.blit(version_text, version_rect)

                if self.menu.current_menu == MenuType.MAIN:
                    # Draw buttons
                    for button in self.menu.main_buttons:
                        is_hovered = button.check_hover(pygame.mouse.get_pos())
                        button.draw(self.screen, is_hovered)
                elif self.menu.current_menu == MenuType.OPTIONS:
                    self.menu.draw_options()
                elif self.menu.current_menu == MenuType.HIGH_SCORES:
                    self.menu.draw_high_scores()

                pygame.display.flip()

            # Control frame rate
            self.clock.tick(30)
        # Handle menu choice
        if menu_choice in ["single_player", "host_game", "join_game"]:
            self.initialize_game()
            self.game_state = GameState.PLAYING

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

    def handle_game_over_state(self):
        # Game over screen
        game_over_active = True
        # Clear event queue before showing game over screen
        pygame.event.clear()
        while game_over_active and not self.quit_game:
            # Process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game = True
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    game_over_active = False
                    self.game_state = GameState.MENU

            # Draw game over screen
            self.screen.fill(Color.WHITE)

            font = pygame.font.SysFont(None, 72)
            game_over_text = font.render("GAME OVER", True, Color.BLACK)
            final_score = font.render(f"Final Score: {self.score}", True, Color.BLACK)

            # Add instructions
            instructions_font = pygame.font.SysFont(None, 32)
            instructions = instructions_font.render("Press any key to continue", True, Color.BLACK)

            self.screen.blit(game_over_text, (WINDOW_WIDTH // 2 - 200, WINDOW_HEIGHT // 2 - 50))
            self.screen.blit(final_score, (WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2 + 20))
            self.screen.blit(instructions, (WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2 + 80))

            pygame.display.flip()
            self.clock.tick(30)
