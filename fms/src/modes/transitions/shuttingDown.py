from modes.mode_classes import State, Transition

from core.eventbus.events import GeneralEvent

class ShuttingDown(Transition):
    def execute(self, state_from: State, fms=None) -> State:
        # Since there's only one state that will go into ShuttingDown, we can ignore state_from

        # Perform shutting down actions here
        fms.emit(GeneralEvent.INFO, {"message": "System is shutting down."})

        # After shutting down, go to off
        from modes.states.off import Off
        return Off()