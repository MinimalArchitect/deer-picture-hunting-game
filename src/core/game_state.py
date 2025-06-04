"""
Abstract base class for all game states.
Defines the interface that all states must implement.
"""

from abc import ABC, abstractmethod
import pygame
from typing import Optional, Any, Dict


class GameState(ABC):
    """
    Abstract base class for all game states.
    
    Each state represents a distinct mode of the game (menu, playing, paused, etc.)
    and handles its own logic, rendering, and events.
    """
    
    def __init__(self, game_context: 'Game'):
        """
        Initialize the state with access to the game context.
        
        Args:
            game_context: Reference to the main Game instance for shared resources
        """
        self.game = game_context
        self.screen = game_context.screen
        self.clock = game_context.clock
        self.is_active = False
        self.state_data = {}  # For storing state-specific data
    
    @abstractmethod
    def enter(self, previous_state: Optional['GameState'] = None, **kwargs) -> None:
        """
        Called when entering this state.
        
        Args:
            previous_state: The state we're transitioning from (if any)
            **kwargs: Additional data passed during state transition
        """
        self.is_active = True
        print(f"Entering {self.__class__.__name__}")
    
    @abstractmethod
    def exit(self, next_state: Optional['GameState'] = None) -> None:
        """
        Called when leaving this state.
        
        Args:
            next_state: The state we're transitioning to (if any)
        """
        self.is_active = False
        print(f"Exiting {self.__class__.__name__}")
    
    @abstractmethod
    def update(self, dt: float) -> Optional[str]:
        """
        Update the state logic.
        
        Args:
            dt: Delta time since last update in seconds
            
        Returns:
            Name of state to transition to, or None to stay in current state
        """
        pass
    
    @abstractmethod
    def render(self) -> None:
        """
        Render the state to the screen.
        This method should handle all drawing for this state.
        """
        pass
    
    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        """
        Handle a pygame event.
        
        Args:
            event: The pygame event to handle
            
        Returns:
            Name of state to transition to, or None to stay in current state
        """
        # Handle common events that all states might need
        if event.type == pygame.QUIT:
            return "quit"
        return None
    
    def get_state_data(self, key: str, default: Any = None) -> Any:
        """Get state-specific data."""
        return self.state_data.get(key, default)
    
    def set_state_data(self, key: str, value: Any) -> None:
        """Set state-specific data."""
        self.state_data[key] = value
    
    def clear_state_data(self) -> None:
        """Clear all state-specific data."""
        self.state_data.clear()


class TransitionableState(GameState):
    """
    Extended state class with built-in transition management.
    Useful for states that need to track transition requests.
    """
    
    def __init__(self, game_context: 'Game'):
        super().__init__(game_context)
        self.transition_request = None
        self.transition_data = {}
    
    def request_transition(self, target_state: str, **kwargs) -> None:
        """
        Request a transition to another state.
        
        Args:
            target_state: Name of the state to transition to
            **kwargs: Additional data to pass to the target state
        """
        self.transition_request = target_state
        self.transition_data = kwargs
        print(f"{self.__class__.__name__} requesting transition to {target_state}")
    
    def check_transition(self) -> Optional[str]:
        """
        Check if a transition has been requested.
        
        Returns:
            Target state name if transition requested, None otherwise
        """
        if self.transition_request:
            target = self.transition_request
            self.transition_request = None
            return target
        return None
    
    def get_transition_data(self) -> Dict[str, Any]:
        """Get data to pass to the next state."""
        data = self.transition_data.copy()
        self.transition_data.clear()
        return data