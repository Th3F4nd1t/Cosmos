from modes.mode_classes import Trigger

class TurnOff(Trigger):
    def check(self, fms=None):
        if fms.turn_off:
            self.active = True
            fms.turn_off = False