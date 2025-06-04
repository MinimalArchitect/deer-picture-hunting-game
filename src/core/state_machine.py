"""
State machine for managing game states and transitions.
Provides centralized state management and clean transitions.
"""

import pygame
from typing import Dict, Optional, Any
from src.core.game_state import GameState


class StateMachine:
    """
    Manages game states and handles transitions between them.
    
    Provides a centralized way to manage state changes, ensuring
    proper cleanup and initialization during transitions.
    """
    
    def __init__(self, game_context: 'Game'):
        """
        Initialize the state machine.
        
        Args:
            game_context: Reference to the main Game instance
        """
        self.game = game_context
        self.states: Dict[str, GameState] = {}
        self.current_state: Optional[GameState] = None
        self.previous_state: Optional[GameState] = None
        self.transition_data: Dict[str, Any] = {}
        self.running = True
    
    def add_state(self, name: str, state: GameState) -> None:
        """
        Add a state to the state machine.
        
        Args:
            name: Unique identifier for the state
            state: The state instance to add
        """
        self.states[name] = state
        print(f"Added state: {name}")
    
    def remove_state(self, name: str) -> None:
        """
        Remove a state from the state machine.
        
        Args:
            name: Name of the state to remove
        """
        if name in self.states:
            if self.current_state == self.states[name]:
                print(f"Warning: Removing current state {name}")
                self.current_state = None
            del self.states[name]
            print(f"Removed state: {name}")
    
    def change_state(self, name: str, **kwargs) -> bool:
        """
        Change to a different state.
        
        Args:
            name: Name of the state to change to
            **kwargs: Additional data to pass to the new state
            
        Returns:
            True if transition was successful, False otherwise
        """
        # Handle special quit state
        if name == "quit":
            self.running = False
            return True
        
        # Check if target state exists
        if name not in self.states:
            print(f"Error: State '{name}' not found")
            return False
        
        # Don't transition to the same state
        if self.current_state == self.states[name]:
            print(f"Already in state {name}")
            return False
        
        # Exit current state
        if self.current_state:
            print(f"Transitioning from {self.current_state.__class__.__name__} to {name}")
            self.current_state.exit(self.states[name])
            self.previous_state = self.current_state
        else:
            print(f"Initial transition to {name}")
        
        # Store transition data
        self.transition_data = kwargs
        
        # Enter new state
        new_state = self.states[name]
        new_state.enter(self.previous_state, **kwargs)
        self.current_state = new_state
        
        # Clear transition data after use
        self.transition_data.clear()
        
        return True
    
    def update(self, dt: float) -> None:
        """
        Update the current state.
        
        Args:
            dt: Delta time since last update in seconds
        """
        if not self.current_state or not self.running:
            return
        
        # Update current state and check for transition request
        transition_request = self.current_state.update(dt)
        
        # Handle transition request
        if transition_request:
            # If state implements TransitionableState, get transition data
            transition_data = {}
            if hasattr(self.current_state, 'get_transition_data'):
                transition_data = self.current_state.get_transition_data()
            
            self.change_state(transition_request, **transition_data)
    
    def render(self) -> None:
        """Render the current state."""
        if self.current_state and self.running:
            self.current_state.render()
    
    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Handle a pygame event.
        
        Args:
            event: The pygame event to handle
        """
        if not self.current_state or not self.running:
            return
        
        # Let current state handle the event
        transition_request = self.current_state.handle_event(event)
        
        # Handle transition request
        if transition_request:
            # If state implements TransitionableState, get transition data
            transition_data = {}
            if hasattr(self.current_state, 'get_transition_data'):
                transition_data = self.current_state.get_transition_data()
            
            self.change_state(transition_request, **transition_data)
    
    def get_current_state_name(self) -> Optional[str]:
        """
        Get the name of the current state.
        
        Returns:
            Name of current state, or None if no current state
        """
        if not self.current_state:
            return None
        
        # Find the name of the current state
        for name, state in self.states.items():
            if state == self.current_state:
                return name
        return None
    
    def get_previous_state_name(self) -> Optional[str]:
        """
        Get the name of the previous state.
        
        Returns:
            Name of previous state, or None if no previous state
        """
        if not self.previous_state:
            return None
        
        # Find the name of the previous state
        for name, state in self.states.items():
            if state == self.previous_state:
                return name
        return None
    
    def is_running(self) -> bool:
        """Check if the state machine is still running."""
        return self.running
    
    def shutdown(self) -> None:
        """Shutdown the state machine and clean up."""
        if self.current_state:
            self.current_state.exit()
            self.current_state = None
        
        self.previous_state = None
        self.running = False
        print("State machine shutdown")


class StateTransition:
    """
    Helper class for defining state transitions with conditions.
    Can be used for more complex transition logic in the future.
    """
    
    def __init__(self, from_state: str, to_state: str, condition: callable = None):
        """
        Initialize a state transition.
        
        Args:
            from_state: Source state name
            to_state: Target state name  
            condition: Optional condition function that must return True for transition
        """
        self.from_state = from_state
        self.to_state = to_state
        self.condition = condition or (lambda: True)
    
    def can_transition(self, current_state: str, context: Any = None) -> bool:
        """
        Check if this transition is valid.
        
        Args:
            current_state: Current state name
            context: Optional context for condition evaluation
            
        Returns:
            True if transition is allowed, False otherwise
        """
        return (current_state == self.from_state and 
                self.condition(context) if context else self.condition())