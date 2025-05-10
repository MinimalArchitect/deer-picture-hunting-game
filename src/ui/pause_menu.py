from direct.gui.DirectGui import DirectFrame, DirectButton, DirectLabel
from panda3d.core import TransparencyAttrib

from src.core.game_state import GameState


class PauseMenu:
    def __init__(self, game_state: GameState):
        self.game_state = game_state
        self.pause_frame = DirectFrame(
            frameSize=(-0.5, 0.5, -0.3, 0.3),
            frameColor=(0, 0, 0, 0.7),
            pos=(0, 0, 0),
            relief="raised"
        )
        self.pause_frame.setTransparency(TransparencyAttrib.M_alpha)
        self.__set_state(game_state.is_paused)

        self.pause_label = DirectLabel(
            parent=self.pause_frame,
            text="Pause Menü",
            scale=0.1,
            pos=(0, 0, 0.2)
        )

        self.resume_button = DirectButton(
            parent=self.pause_frame,
            text="Fortsetzen",
            scale=0.08,
            pos=(0, 0, 0),
            command=self.toggle_pause
        )

        self.exit_button = DirectButton(
            parent=self.pause_frame,
            text="Beenden",
            scale=0.08,
            pos=(0, 0, -0.2),
            command=self.quit_game
        )

        game_state.base.accept("escape", self.toggle_pause)

    def __set_state(self, hidden=True):
        if hidden:
            self.pause_frame.show()
        else:
            self.pause_frame.hide()

    def toggle_pause(self):
        """Toggles the pause menu and sets the `is_paused` flag in the game state to the same value."""
        self.game_state.is_paused = not self.game_state.is_paused

        if self.game_state.is_paused:
            self.pause_frame.show()
        else:
            self.pause_frame.hide()

    def quit_game(self):
        self.game_state.base.userExit()
