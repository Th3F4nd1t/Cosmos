from modes.mode_classes import State



class Modeless(State):
    def attach_triggers(self, fms=None):
        from modes.triggers.turnOff import TurnOff
        fms.set_triggers({"TurnOff": TurnOff()})

    def execute(self, fms=None):
        if fms.getTrigger("TurnOff").get():
            fms.getTrigger("TurnOff").reset()
            from modes.transitions.shuttingDown import ShuttingDown
            return ShuttingDown()
        return None