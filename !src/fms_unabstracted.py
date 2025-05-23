from states import StateHandler, States
from queue import Queue, PriorityQueue
from threading import Thread
from switches import Switch, SwitchConfig, SwitchHandler, SwitchType
from constants.ip import IP
from configs.config import Config

# Cisco 3850 switch configuration
main_switch_config = """

"""

class FMS:
    def __init__(self):
        self.red_switch = None
        self.blue_switch = None
        self.state_handler = StateHandler()
        self.logger = Logger("FMS")
        self.logger.log("FMS initialized")
        self.queue = Queue()
        self.priority_queue = PriorityQueue()
        self._set_teams(1, 2, 3, 4, 5, 6)
        self._init_switches()

    def _set_teams(self, red1: int, red2: int, red3: int, blue1: int, blue2: int, blue3: int):
        self.red1 = red1
        self.red2 = red2
        self.red3 = red3
        self.blue1 = blue1
        self.blue2 = blue2
        self.blue3 = blue3
        self.ips = {
            "red_1": IP.DS(red1),
            "red_2": IP.DS(red2),
            "red_3": IP.DS(red3),
            "blue_1": IP.DS(blue1),
            "blue_2": IP.DS(blue2),
            "blue_3": IP.DS(blue3)
        }
        
    def _init_switches(self):
        self.switch_handler = SwitchHandler()
        main_switch = Switch("MainSwitch", IP.MAIN_SWITCH)
        red_switch = Switch("RedSwitch", IP.RED_SWITCH)
        blue_switch = Switch("BlueSwitch", IP.BLUE_SWITCH)
        self.switch_handler.add_switch(main_switch)
        self.switch_handler.add_switch(red_switch)
        self.switch_handler.add_switch(blue_switch)

        self.switch_handler.add_config("MainSwitch", Config(self.ips).MAIN)
        self.switch_handler.add_config("RedSwitch", Config(self.ips).RED)
        self.switch_handler.add_config("BlueSwitch", Config(self.ips).BLUE)

        self.switch_handler.push_config()
        self.logger.log("Switches initialized and configured")


