class State:
    """
    Represents a mode of the FMS in which a constant action is being performed. Moved into from a known "physical" state.
    """
    def attach_triggers(self, fms=None):
        """Attach triggers to the state. Ran once when the state is entered."""
        raise NotImplementedError
    
    def execute(self, fms=None) -> "Transition":
        """Looped through as fast as possible while in the state. Should be non-blocking and check for triggers as well. When a trigger is met, it should return the transition to move to, otherwise return None."""
        raise NotImplementedError

class Transition:
    """
    Represents a change from one State to another. Getting into a known "physical" state. Should return the state to move to when complete.
    """
    def execute(self, state_from: State, fms=None) -> State:
        """Run the transition. Should be blocking until the transition is complete, then return the new State to move to."""
        raise NotImplementedError

class Trigger:
    """
    Represents something that the FMS should check for each cycle to determine if a mode needs to be changed to. Context specific.
    """
    def __init__(self):
        self.active = False

    def check(self, fms=None):
        """Check if the trigger condition is met. Ran by FMS every cycle when attached."""
        raise NotImplementedError
    
    def get(self) -> bool:
        return self.active

    def reset(self):
        self.active = False
