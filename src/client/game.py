import json
import os
from abc import ABC, abstractmethod

import pygame
import validators
from PodSixNet.Connection import ConnectionListener, connection
from pygame.event import Event
from validators import ValidationError

from src.client.game_map import GameMap
from src.core.config import GameConfig, GameClientConfig
from src.core.enum import MoveDirection, PlayerColor
from src.core.type import Position
from src.ui.button import DefaultButtonConfig, Button
from src.ui.gamefont import GameFont
from src.util.color import Color
from src.util.sound import Sound
from src.util.texture import Texture


class GameObject(ABC):
    def __init__(self, position: Position, direction: MoveDirection) -> None:
        """
        Precondition:
            - position is a valid Position object
            - direction is a valid MoveDirection

        Postcondition:
            - self._position and self._direction are initialized with given values
        """
        self._position = position
        self._direction = direction

    @property
    def position(self) -> Position:
        """
        Postcondition:
            - Returns the current position of the GameObject
        """
        return self._position


class Player(GameObject):
    def __init__(self, position: Position, direction: MoveDirection) -> None:
        """
        Precondition:
            - position and direction must be valid

        Postcondition:
            - Player is correctly initialized via GameObject constructor
        """
        super().__init__(position, direction)

    def draw(self, surface, color: PlayerColor) -> None:
        """
        Precondition:
            - surface is a valid Pygame surface
            - color is a valid PlayerColor

        Postcondition:
            - Draws the player sprite on the given surface based on direction
        """
        pos = (self.position.x * GameClientConfig.TILE_SIZE, self.position.y * GameClientConfig.TILE_SIZE)
        if self._direction == MoveDirection.UP:
            surface.blit(Texture.hunter[color].back, pos)
        if self._direction == MoveDirection.DOWN:
            surface.blit(Texture.hunter[color].front, pos)
        if self._direction == MoveDirection.LEFT:
            surface.blit(Texture.hunter[color].left, pos)
        if self._direction == MoveDirection.RIGHT:
            surface.blit(Texture.hunter[color].right, pos)


class Deer(GameObject):
    def __init__(self, position: Position, direction: MoveDirection) -> None:
        """
        Precondition:
            - position and direction must be valid

        Postcondition:
            - Deer is correctly initialized via GameObject constructor
        """
        super().__init__(position, direction)

    def draw(self, surface):
        """
        Precondition:
            - surface is a valid Pygame surface

        Postcondition:
            - Draws the deer sprite on the given surface at current position
        """
        pos = (self.position.x * GameClientConfig.TILE_SIZE, self.position.y * GameClientConfig.TILE_SIZE)
        surface.blit(Texture.deer, pos)


class GameClientContext(ConnectionListener):
    def __init__(self, server_host: tuple[str, int], is_sound_enabled: bool):
        """
        Precondition:
            - server_host is a tuple of (host, port)
            - is_sound_enabled is a boolean

        Postcondition:
            - GameClientContext is initialized and attempts to connect to server
        """
        self.map: GameMap | None = None
        self.players: list[Player] = []
        self.deer: list[Deer] = []
        self.score: int = 0
        self.time_left: float = GameClientConfig.GAME_DURATION
        self.server_host: tuple[str, int]
        self.level: int | None = None

        self.is_disconnected = False
        self._is_server_playing_game = False

        self.is_sound_enabled = is_sound_enabled

        self.Connect(server_host)

    def pump(self):
        """
        Postcondition:
            - Processes incoming and outgoing network messages
        """
        connection.Pump()
        self.Pump()

    def send_move(self, move_direction: MoveDirection):
        """
        Precondition:
            - move_direction is a valid MoveDirection

        Postcondition:
            - Sends a move action to the server
        """
        self.Send({
            'action': 'move',
            'move_direction': move_direction.name,
        })

    def send_take_picture(self):
        """
        Postcondition:
            - Sends a take_picture action to the server
        """
        self.Send({
            'action': 'take_picture'
        })

    def send_select_level(self, level: int):
        """
        Precondition:
            - level is within GameClientConfig.MIN_LEVEL and MAX_LEVEL

        Postcondition:
            - Sends a select_level request to the server
        """
        assert GameClientConfig.MIN_LEVEL <= level <= GameClientConfig.MAX_LEVEL
        connection.Send({
            'action': 'select_level',
            'level': level,
        })

    def Network_game_started(self, data):
        """
        Precondition:
            - data contains a valid level

        Postcondition:
            - Initializes game map and level
        """
        self.map = GameMap(level=data['level'])
        self.level = data['level']

    def Network_state_update(self, data):
        """
        Precondition:
            - data['message'] contains valid player and deer states

        Postcondition:
            - Updates the game state with new player, deer positions and time left
        """
        print('Here is the state update:', data['message'])
        self.players = [Player(Position(position['x'], position['y']), MoveDirection.__dict__[position['direction'].upper()]) for position in
                        data['message']['players']]
        self.deer = [Deer(Position(position['x'], position['y']), MoveDirection.__dict__[position['direction'].upper()]) for position in
                     data['message']['deer']]
        self.time_left = float(data['message']['time_left'])

    def Network_score(self, data):
        """
        Precondition:
            - data contains a valid score

        Postcondition:
            - Updates current score and sets server as not playing
        """
        self.score = data['score']
        self._is_server_playing_game = False

    def Network_connected(self, data):
        """
        Postcondition:
            - Logs successful server connection
        """
        print('You are now connected to the server')

    def Network_error(self, data):
        """
        Precondition:
            - data contains error details

        Postcondition:
            - Logs error and disconnects client
        """
        print('error:', data['error'])
        connection.Close()
        self.is_disconnected = True

    def Network_moved(self, data):
        """
        Postcondition:
            - Plays move sound if sound is enabled
        """
        if self.is_sound_enabled:
            Sound.move.play()

    def Network_picture_taken(self, data):
        """
        Postcondition:
            - Plays photo sound if sound is enabled
        """
        if self.is_sound_enabled:
            Sound.take_photo.play()

    def Network_disconnected(self, data):
        """
        Postcondition:
            - Logs disconnect and updates state
        """
        print('Server disconnected')
        self.is_disconnected = True

    def Disconnect(self):
        """
        Postcondition:
            - Closes the connection
        """
        connection.Close()

    @property
    def is_server_playing_game(self):
        """
        Postcondition:
            - Returns the server's playing status
        """
        return self._is_server_playing_game

    @is_server_playing_game.setter
    def is_server_playing_game(self, value):
        """
        Precondition:
            - value is a boolean

        Postcondition:
            - Updates the server playing status
        """
        self._is_server_playing_game = value


class GameContext:
    def __init__(self):
        """
        Postcondition:
            - Initializes game window, clock, and sound settings
        """
        self.client_config = GameClientConfig()
        self.client_context: GameClientContext | None = None

        self._is_running = True

        self.clock = pygame.time.Clock()
        self.frame_rate = 30

        self.screen = pygame.display.set_mode((GameClientConfig.WINDOW_WIDTH, GameClientConfig.WINDOW_HEIGHT))
        pygame.display.set_caption('Deer Picture Hunting')

        self.is_sound_enabled = True

    @property
    def is_running(self) -> bool:
        """
        Postcondition:
            - Returns whether the game is currently running
        """
        return self._is_running

    @is_running.setter
    def is_running(self, value):
        """
        Precondition:
            - value is a boolean

        Postcondition:
            - Updates the game running status
        """
        self._is_running = value


class GameState(ABC):
    def __init__(self):
        """
        Postcondition:
            - Initializes the transition request as None
        """
        self._transition_request: type[GameState] | None = None

    @abstractmethod
    def enter(self, old_state: type['GameState'] | None, context: GameContext) -> None:
        """
        Precondition:
            - context is a valid GameContext object
        Postcondition:
            - Performs logic necessary when entering a game state
        """
        pass

    @abstractmethod
    def exit(self, context: GameContext) -> None:
        """
        Precondition:
            - context is a valid GameContext object
        Postcondition:
            - Performs logic necessary when exiting a game state
        """
        pass

    @abstractmethod
    def handle_events(self, events: list[Event], context: GameContext) -> None:
        """
        Precondition:
            - events is a list of Pygame events
            - context is a valid GameContext object
        Postcondition:
            - Processes relevant events for the current game state
        """
        pass

    @abstractmethod
    def update(self, dt: float, context: GameContext) -> None:
        """
        Precondition:
            - dt is the delta time (float), context is valid GameContext
        Postcondition:
            - Updates the game state logic based on elapsed time
        """
        pass

    @abstractmethod
    def render(self, context: GameContext) -> None:
        """
        Precondition:
            - context is a valid GameContext object
        Postcondition:
            - Renders the visual state to the screen
        """
        pass

    @property
    def transition_request(self):
        """
        Postcondition:
            - Returns the requested transition target (if any)
        """
        return self._transition_request


class Scores:
    def __init__(self):
        """
        Postcondition:
            - Initializes score file path and resets score dictionary
        """
        self.score_file = GameClientConfig.SCORE_FILE

        self.level_scores: dict[str, int] = {}
        self.reset_scores()

    def reset_scores(self):
        """
        Postcondition:
            - Resets scores for all levels to 0
        """
        self.level_scores = {}  # {level_number: highest_score}
        for level in range(GameConfig.MIN_LEVEL, GameConfig.MAX_LEVEL + 1, 1):
            self.level_scores[f'{level}'] = 0

    def load_scores(self):
        """
        Postcondition:
            - Loads scores from file if present; else resets and saves scores
        """
        self.level_scores = {}
        if os.path.exists(self.score_file):
            try:
                with open(self.score_file, 'r') as f:
                    self.level_scores = json.load(f)
            except Exception as e:
                print('Error loading scores:', e)
        else:
            self.reset_scores()
            self.save_scores()

    def save_scores(self):
        """
        Postcondition:
            - Saves the current scores to disk in JSON format
        """
        try:
            with open(self.score_file, 'w') as f:
                # Ensure keys are strings for JSON compatibility
                json.dump({str(k): v for k, v in self.level_scores.items()}, f)
        except Exception as e:
            print('Error saving scores:', e)

    def get(self, level: int) -> int:
        """
        Precondition:
            - GameClientConfig.MIN_LEVEL <= level <= GameClientConfig.MAX_LEVEL
        Postcondition:
            - Returns high score for the given level
        """
        assert GameClientConfig.MIN_LEVEL <= level <= GameClientConfig.MAX_LEVEL
        return self.level_scores[str(level)]

    def set_high_score(self, level: int, score: int) -> None:
        """
        Precondition:
            - GameClientConfig.MIN_LEVEL <= level <= GameClientConfig.MAX_LEVEL
        Postcondition:
            - Sets the new high score if it's higher than the existing one
        """
        assert GameClientConfig.MIN_LEVEL <= level <= GameClientConfig.MAX_LEVEL
        self.level_scores[str(level)] = max(score, self.level_scores[str(level)])


class MainMenuState(GameState):
    def __init__(self):
        """
        Postcondition:
            - Initializes all menu buttons with correct positions and labels
        """
        super().__init__()

        self.center_x = GameClientConfig.WINDOW_WIDTH // 2
        button_x = self.center_x - DefaultButtonConfig.default_width // 2

        self.join_game_button = Button('Join Game', button_x, 290)
        self.options_button = Button('Options', button_x, 360)
        self.high_score_button = Button('High Scores', button_x, 430)
        self.exit_button = Button('Exit', button_x, 500)

    def enter(self, old_state: GameState, context: GameContext) -> None:
        """
        Precondition:
            - context.client_context is None
        Postcondition:
            - Ready to display main menu
        """
        assert context.client_context is None

    def exit(self, context: GameContext) -> None:
        """
        Precondition:
            - context.client_context is None
        Postcondition:
            - Leaves the main menu state
        """
        assert context.client_context is None

    def handle_events(self, events: list[Event], context: GameContext) -> None:
        """
        Precondition:
            - events is a list of Pygame events
        Postcondition:
            - Sets transition request based on clicked button
        """
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                if self.join_game_button.is_clicked(mouse_position):
                    self._transition_request = ServerSelectionMenuState
                elif self.options_button.is_clicked(mouse_position):
                    self._transition_request = OptionsMenuState
                elif self.high_score_button.is_clicked(mouse_position):
                    self._transition_request = HighScoreMenuState
                elif self.exit_button.is_clicked(mouse_position):
                    context.is_running = False

    def update(self, dt: float, context: GameContext) -> None:
        pass

    def render(self, context: GameContext) -> None:
        """
        Postcondition:
            - Renders menu title, version, and buttons
        """
        # Draw title
        title_text = GameFont.heading1_font.render('Deer Picture Hunting', True, Color.BLACK)
        title_rect = title_text.get_rect(center=(self.center_x, 80))
        context.screen.blit(title_text, title_rect)

        # Draw version text
        version_text = GameFont.version_font.render('2D Grid-Based Version', True, Color.BLACK)
        version_rect = version_text.get_rect(center=(self.center_x, 120))
        context.screen.blit(version_text, version_rect)

        # Draw buttons
        for button in [
            self.join_game_button,
            self.options_button,
            self.high_score_button,
            self.exit_button
        ]:
            button.draw(context.screen, button.check_hover(pygame.mouse.get_pos()))


class HighScoreMenuState(GameState):
    def __init__(self):
        """
        Postcondition:
            - Initializes score display and control buttons
        """
        super().__init__()
        self.scores = Scores()
        self.scores.load_scores()

        center_x = GameClientConfig.WINDOW_WIDTH // 2 - DefaultButtonConfig.default_width // 2
        self.back_button = Button('Back', center_x - DefaultButtonConfig.default_width // 2 - 10, 500)
        self.reset_button = Button('Reset', center_x + DefaultButtonConfig.default_width // 2 + 10, 500)

    def enter(self, old_state: type[GameState] | None, context: GameContext) -> None:
        """
        Precondition:
            - context.client_context is None
        Postcondition:
            - Ready to show high scores
        """
        assert context.client_context is None

    def exit(self, context: GameContext) -> None:
        """
        Precondition:
            - context.client_context is None
        Postcondition:
            - Leaves high score menu
        """
        assert context.client_context is None

    def handle_events(self, events: list[Event], context: GameContext) -> None:
        """
        Postcondition:
            - Handles back/reset button clicks
        """
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                if self.back_button.is_clicked(mouse_position):
                    self._transition_request = MainMenuState
                elif self.reset_button.is_clicked(mouse_position):
                    self.scores.reset_scores()
                    self.scores.save_scores()

    def update(self, dt: float, context: GameContext) -> None:
        pass

    def render(self, context: GameContext) -> None:
        """
        Postcondition:
            - Renders all high scores and buttons
        """
        # Draw title
        title_text = GameFont.heading1_font.render('High Scores', True, Color.BLACK)
        title_rect = title_text.get_rect(center=(GameClientConfig.WINDOW_WIDTH // 2, 60))
        context.screen.blit(title_text, title_rect)

        # Draw scores in two columns
        column_x = [GameClientConfig.WINDOW_WIDTH // 2 - 180, GameClientConfig.WINDOW_WIDTH // 2 + 20]
        y_start = 140
        line_spacing = 30

        for i, level in enumerate(range(1, 21)):
            col = 0 if level <= GameClientConfig.MAX_LEVEL // 2 else 1
            row = i if level <= GameClientConfig.MAX_LEVEL // 2 else i - GameClientConfig.MAX_LEVEL // 2
            y = y_start + row * line_spacing
            score = self.scores.get(level)
            text = f'Level {level}: {score if score is not None else '-'}'
            line = GameFont.text_font.render(text, True, Color.BLACK)
            context.screen.blit(line, (column_x[col], y))

        for button in [self.back_button, self.reset_button]:
            button.draw(context.screen, button.check_hover(pygame.mouse.get_pos()))


class OptionsMenuState(GameState):
    def __init__(self):
        """
        Postcondition:
            - Initializes back and sound toggle buttons
        """
        super().__init__()
        center_x = GameClientConfig.WINDOW_WIDTH // 2 - DefaultButtonConfig.default_width // 2

        self.back_button = Button('Back', center_x, 400)
        self.sound_toggle_button = Button('Sound: On', center_x, 250)

    def enter(self, old_state: type[GameState] | None, context: GameContext) -> None:
        """
        Precondition:
            - context.client_context is None
        Postcondition:
            - Ready to show options menu
        """
        assert context.client_context is None

    def exit(self, context: GameContext) -> None:
        """
        Precondition:
            - context.client_context is None
        Postcondition:
            - Leaves options menu
        """
        assert context.client_context is None

    def handle_events(self, events: list[pygame.event.Event], context: GameContext) -> None:
        """
        Postcondition:
            - Handles back and sound toggle interactions
        """
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                if self.back_button.is_clicked(mouse_position):
                    self._transition_request = MainMenuState
                if self.sound_toggle_button.is_clicked(mouse_position):
                    context.is_sound_enabled = not context.is_sound_enabled

    def update(self, dt: float, context: GameContext) -> None:
        pass

    def render(self, context: GameContext) -> None:
        """
        Postcondition:
            - Draws title and buttons for options
        """
        title_text = GameFont.heading1_font.render('Options', True, Color.BLACK)
        title_rect = title_text.get_rect(center=(GameClientConfig.WINDOW_WIDTH // 2, 60))
        context.screen.blit(title_text, title_rect)

        self.sound_toggle_button.text = f'Sound: {'On' if context.is_sound_enabled else 'Off'}'

        for button in [self.sound_toggle_button, self.back_button]:
            button.draw(context.screen, button.check_hover(pygame.mouse.get_pos()))


class ServerSelectionMenuState(GameState):
    def __init__(self):
        """
        Postcondition:
            - Initializes input field and menu buttons for server selection
        """
        super().__init__()
        center_x = GameClientConfig.WINDOW_WIDTH // 2 - DefaultButtonConfig.default_width // 2

        self.server_host: str = ''

        # Rectangle position and size
        self.rect_width, self.rect_height = 220, 50
        self.rect_x, self.rect_y = GameClientConfig.WINDOW_WIDTH // 2 - self.rect_width // 2, 250
        self.border_thickness = 4

        self.back_button = Button('Back', center_x - DefaultButtonConfig.default_width // 2 - 10, 400)
        self.join_button = Button('Join', center_x + DefaultButtonConfig.default_width // 2 + 10, 400)
        self.join_button.disable()

    def enter(self, old_state: type[GameState] | None, context: GameContext) -> None:
        """
        Precondition:
            - context.client_context is None
        Postcondition:
            - Ready to enter server address
        """
        assert context.client_context is None

    def exit(self, context: GameContext) -> None:
        pass

    def handle_events(self, events: list[pygame.event.Event], context: GameContext) -> None:
        """
        Postcondition:
            - Handles typing and button interactions
        """
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                if self.back_button.is_clicked(mouse_position):
                    self._transition_request = MainMenuState
                if self.join_button.is_clicked(mouse_position):
                    context.client_context = GameClientContext(server_host=(self.server_host, 12345), is_sound_enabled=context.is_sound_enabled)
                    self._transition_request = LevelSelectionMenuState

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.server_host: str = self.server_host[:-1]
                elif len(self.server_host) < 50:
                    self.server_host += event.unicode

                try:
                    if not self.server_host.isdigit() and validators.hostname(self.server_host, may_have_port=False, consider_tld=True, maybe_simple=True):
                        self.join_button.enable()
                    else:
                        self.join_button.disable()
                except ValidationError:
                    self.join_button.disable()

    def update(self, dt: float, context: GameContext) -> None:
        pass

    def render(self, context: GameContext) -> None:
        """
        Postcondition:
            - Renders input field, entered text, and control buttons
        """
        pygame.draw.rect(
            context.screen,
            (0, 0, 0),
            (self.rect_x, self.rect_y, self.rect_width, self.rect_height)
        )

        ## Draw white rectangle (inside, so border is visible)
        pygame.draw.rect(
            context.screen, (255, 255, 255),
            (
                self.rect_x + self.border_thickness,
                self.rect_y + self.border_thickness,
                self.rect_width - 2 * self.border_thickness,
                self.rect_height - 2 * self.border_thickness
            )
        )

        ## Render input text
        text = GameFont.text_font.render(self.server_host, True, Color.BLACK)
        text_rect = text.get_rect(center=(GameClientConfig.WINDOW_WIDTH // 2, 275))
        context.screen.blit(text, text_rect)

        for button in [self.join_button, self.back_button]:
            button.draw(context.screen, button.check_hover(pygame.mouse.get_pos()))


class LevelSelectionMenuState(GameState):
    def __init__(self):
        """
        Postcondition:
            - Initializes level selection buttons and back button
        """
        super().__init__()
        columns = 5
        spacing = 10
        button_width = 100
        button_height = 40
        start_x = GameClientConfig.WINDOW_WIDTH // 2 - ((columns * button_width) + (columns - 1) * spacing) // 2
        start_y = 180
        total_levels = 20

        button_center_x = GameClientConfig.WINDOW_WIDTH // 2 - DefaultButtonConfig.default_width // 2
        self.back_button = Button(
            "Back",
            button_center_x,
            start_y + ((total_levels // columns) + 2) * (button_height + spacing)
        )

        self.level_buttons = []
        for level in range(total_levels):
            row = level // columns
            col = level % columns
            self.level_buttons.append(Button(
                f"{level + 1}",
                start_x + col * (button_width + spacing), start_y + row * (button_height + spacing),
                button_width,
                button_height
            ))

    def enter(self, old_state: type[GameState] | None, context: GameContext) -> None:
        """
        Precondition:
            - context.client_context is not None
        Postcondition:
            - Ready to select level
        """
        assert context.client_context is not None

    def exit(self, context: GameContext) -> None:
        pass

    def handle_events(self, events: list[pygame.event.Event], context: GameContext) -> None:
        """
        Postcondition:
            - Processes button clicks for level selection or going back
        """
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                if self.back_button.is_clicked(mouse_position):
                    context.client_context.Disconnect()
                    context.client_context = None
                    self._transition_request = MainMenuState
                for level, button in enumerate(self.level_buttons, 1):
                    if button.is_clicked(mouse_position):
                        context.client_context.send_select_level(level)
                        self._transition_request = PlayingState

    def update(self, dt: float, context: GameContext) -> None:
        """
        Postcondition:
            - Updates connection and transitions if map is ready or disconnected
        """
        if context.client_context is None:
            return

        context.client_context.pump()
        if context.client_context.is_disconnected:
            context.client_context = None
            self._transition_request = MainMenuState
            return
        if context.client_context.map:
            self._transition_request = PlayingState

    def render(self, context: GameContext) -> None:
        """
        Postcondition:
            - Renders level buttons and title
        """
        title_text = GameFont.heading1_font.render("Choose Level", True, Color.BLACK)
        title_rect = title_text.get_rect(center=(GameClientConfig.WINDOW_WIDTH // 2, 60))
        context.screen.blit(title_text, title_rect)

        for button in self.level_buttons + [self.back_button]:
            button.draw(context.screen, button.check_hover(pygame.mouse.get_pos()))


class PlayingState(GameState):
    def __init__(self):
        """
        Postcondition:
            - Stores previous frame rate for later restoration
        """
        super().__init__()
        self.previous_frame_rate: int = GameClientConfig.FRAME_RATE

    def enter(self, old_state: type[GameState] | None, context: GameContext) -> None:
        """
        Precondition:
            - context.client_context is not None
        Postcondition:
            - Switches to fast game loop and sets game as playing
        """
        assert context.client_context is not None
        self.previous_frame_rate = context.frame_rate
        context.client_context.is_server_playing_game = True
        context.frame_rate = 60

    def exit(self, context: GameContext) -> None:
        """
        Postcondition:
            - Restores original frame rate
        """
        # assert context.client_context is not None
        context.frame_rate = self.previous_frame_rate

    def handle_events(self, events: list[Event], context: GameContext) -> None:
        """
        Postcondition:
            - Handles movement and picture taking
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    context.client_context.send_take_picture()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            context.client_context.send_move(MoveDirection.UP)
        elif keys[pygame.K_DOWN]:
            context.client_context.send_move(MoveDirection.DOWN)
        elif keys[pygame.K_LEFT]:
            context.client_context.send_move(MoveDirection.LEFT)
        elif keys[pygame.K_RIGHT]:
            context.client_context.send_move(MoveDirection.RIGHT)

    def update(self, dt: float, context: GameContext) -> None:
        """
        Postcondition:
            - Pumps state and transitions to game over or main menu if needed
        """
        if context.client_context is None:
            return

        context.client_context.pump()

        if not context.client_context.is_server_playing_game:
            context.client_context.map = None
            self._transition_request = GameOverState
        if context.client_context.is_disconnected:
            context.client_context = None
            self._transition_request = MainMenuState

    def render(self, context: GameContext) -> None:
        """
        Postcondition:
            - Draws game world and UI elements (score, time)
        """
        if context.client_context is None:
            return
        if context.client_context.map is None:
            return

        context.client_context.map.draw(context.screen)

        colors: list[PlayerColor] = list(PlayerColor)

        [player.draw(context.screen, colors[index]) for index, player in enumerate(context.client_context.players)]
        [deer.draw(context.screen) for deer in context.client_context.deer]

        # Draw UI
        score_text = GameFont.text_font.render(f'High Score: {context.client_context.score}', True, Color.BLACK)
        context.screen.blit(score_text, (10, 10))

        time_text = GameFont.text_font.render(f'Time: {int(context.client_context.time_left)}s', True, Color.BLACK)
        context.screen.blit(time_text, (GameClientConfig.WINDOW_WIDTH - time_text.get_width() - 10, 10))


class GameOverState(GameState):
    def __init__(self):
        """
        Postcondition:
            - Initializes score system for game over screen
        """
        super().__init__()
        self.center_y = GameClientConfig.WINDOW_HEIGHT // 2
        self.scores = Scores()
        self.scores.load_scores()

    def enter(self, old_state: type[GameState] | None, context: GameContext) -> None:
        """
        Postcondition:
            - Stores and saves high score
        """
        self.scores.set_high_score(context.client_context.level, context.client_context.score)
        self.scores.save_scores()
        assert context.client_context is not None

    def exit(self, context: GameContext) -> None:
        """
        Precondition:
            - context.client_context is not None
        Postcondition:
            - Final cleanup before transitioning
        """
        assert context.client_context is not None

    def handle_events(self, events: list[pygame.event.Event], context: GameContext) -> None:
        """
        Postcondition:
            - Waits for any input and then transitions to level selection
        """
        for event in events:
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                self._transition_request = LevelSelectionMenuState

    def update(self, dt: float, context: GameContext) -> None:
        """
        Postcondition:
            - Updates game client network state
        """
        context.client_context.pump()

    def render(self, context: GameContext) -> None:
        """
        Postcondition:
            - Renders final score and message
        """
        game_over_text = GameFont.heading1_font.render('GAME OVER', True, Color.BLACK)
        game_over_text_rect = game_over_text.get_rect(center=(GameClientConfig.WINDOW_WIDTH // 2, GameClientConfig.WINDOW_HEIGHT // 2 - 50))
        context.screen.blit(game_over_text, game_over_text_rect)

        if context.client_context.score == -1:
            final_score_text = GameFont.heading1_font.render(f'You have photographed another player. You lose!', True, Color.BLACK)
            final_score_text_rect = final_score_text.get_rect(center=(GameClientConfig.WINDOW_WIDTH // 2, GameClientConfig.WINDOW_HEIGHT // 2 + 20))
            context.screen.blit(final_score_text, final_score_text_rect)
        else:
            final_score_text = GameFont.heading1_font.render(f'Final Score: {context.client_context.score}', True, Color.BLACK)
            final_score_text_rect = final_score_text.get_rect(center=(GameClientConfig.WINDOW_WIDTH // 2, GameClientConfig.WINDOW_HEIGHT // 2 + 20))
            context.screen.blit(final_score_text, final_score_text_rect)

        instruction_text = GameFont.text_font.render('Press any key to continue', True, Color.BLACK)
        instruction_text_rect = final_score_text.get_rect(center=(GameClientConfig.WINDOW_WIDTH // 2, GameClientConfig.WINDOW_HEIGHT // 2 + 80))
        context.screen.blit(instruction_text, instruction_text_rect)


class Game:
    def __init__(self):
        """
        Postcondition:
            - Initializes Pygame and game subsystems
        """
        pygame.init()
        pygame.mixer.init()

        self.context = GameContext()

        Texture.load_all()
        Sound.load_all()
        GameFont.load_all()

        self.current_state: GameState = MainMenuState()
        self.old_state: GameState | None = None
        self._passed_time = 0

    def update(self):
        """
        Postcondition:
            - Processes events, updates game logic, renders, and handles state transitions
        """
        # handle_events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.context.is_running = False
                break
        self.current_state.handle_events(events, self.context)

        # update
        self.current_state.update(self._passed_time, self.context)

        # render
        self.context.screen.fill(Color.BACKGROUND)
        self.current_state.render(self.context)

        # state transitions
        next_state = self.current_state.transition_request

        if next_state is not None:
            self.old_state = type(self.current_state)
            self.current_state.exit(self.context)
            self.current_state = next_state()
            pygame.event.clear()
            self.current_state.enter(self.old_state, self.context)

        # tick
        pygame.display.flip()
        self._passed_time = self.context.clock.tick(self.context.frame_rate)

    def shutdown(self):
        """
        Postcondition:
            - Performs final cleanup of game state
        """
        if self.current_state:
            self.current_state.exit(self.context)
        print('State machine shutdown')

    def run(self):
        """
        Postcondition:
            - Runs main game loop until the game is stopped
        """
        while self.context.is_running:
            self.update()

        self.shutdown()
