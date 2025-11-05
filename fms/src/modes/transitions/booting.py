from modes.mode_classes import State, Transition
from modes.states.modeless import Modeless

from core.eventbus.events import GeneralEvent

class Booting(Transition):
    def execute(self, state_from: State, fms=None) -> State:
        # Since there's only one state that will go into Booting, we can ignore state_from

        # Perform booting actions here
        fms.emit(GeneralEvent.INFO, {"message": "System is booting up."})

        # After booting, go to modeless
        return Modeless()