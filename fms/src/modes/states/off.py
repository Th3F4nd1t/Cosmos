from modes.mode_classes import State


class Off(State):
    def attach_triggers(self, fms=None):
        from modes.triggers.turnOn import TurnOn
        fms.set_triggers({"TurnOn": TurnOn()})

    def execute(self, fms=None):
        if fms.getTrigger("TurnOn").get():
            fms.getTrigger("TurnOn").reset()
            from modes.transitions.booting import Booting
            return Booting()
        return None