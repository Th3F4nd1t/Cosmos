from modes.mode_classes import Trigger

class TurnOn(Trigger):
    def check(self, fms=None):
        if fms.turn_on:
            self.active = True
            fms.turn_on = False
        