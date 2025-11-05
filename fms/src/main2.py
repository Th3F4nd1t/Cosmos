# External imports
import threading
import time
import traceback

# Internal imports
from core.eventbus.event_bus import EventBus
from core.eventbus.events import GeneralEvent, EventBusEvent, MatchEvent, RobotEvent, PLCEvent, StateEvent, SwitchEvent, TeamEvent, UserAttentionEvent, TerminalEvent
from core.match_controller import MatchController
from core.state_store import StateStore, States
from core.plc_handler import PLCHandler
from core.switch_handler import SwitchHandler
from core.station_manager import StationManager

from utils.ip import ip, driverstation_ip, IP
from utils.config_loader import load_config
# from utils.teams import TeamsManager, TeamData
from utils.user_attention import UserAttentionQueue # Possible future removal

from tools.terminal.socket_server import SocketServer

from modes.mode_classes import *
from modes.states import off
from modes.transitions import *
from modes.triggers import *


class FMS:
    def __init__(self):
        self.mode: State | Transition = off.Off()
        self.triggers: dict[str, Trigger] = {}

        # Exception queue for storing errors in (e, tb)
        self.exception_queue = []

        # Event bus for handling events
        self.event_bus = EventBus()
        threading.Thread(target=self.event_bus.run, daemon=True).start()
        self.emit(GeneralEvent.DEBUG, {"message": "Event bus initialized"})
        self._attach_subscribers()

        # User attention queue for handling things that need user attention; can be accessed via terminals or via web gui
        self.user_attention = UserAttentionQueue()
        self.emit(GeneralEvent.DEBUG, {"message": "User attention queue initialized"})

        # Create state store instance
        self.state_store = StateStore()
        self.emit(GeneralEvent.DEBUG, {"message": "State store initialized"})


        # Simple thread-safe socket server to get/set two variables (A and B)
        self.var_lock = threading.Lock()
        self.turn_on = False
        self.turn_off = False

        self.socket_server = SocketServer(self)
        threading.Thread(target=self.socket_server.run, daemon=True).start()

        self.pin = None


    def _notify_error(self, data: dict):
        print(f"[ERROR] {data.get('message', '')}")
    def _notify_warning(self, data: dict):
        print(f"[WARNING] {data.get('message', '')}")
    def _notify_info(self, data: dict):
        print(f"[INFO] {data.get('message', '')}")
    def _notify_debug(self, data: dict):
        print(f"[DEBUG] {data.get('message', '')}")

    def _attach_subscribers(self):
        """
        Attach subscribers to the event bus.
        """
        self.event_bus.subscribe(GeneralEvent.ERROR, self._notify_error)
        self.event_bus.subscribe(GeneralEvent.WARNING, self._notify_warning)
        self.event_bus.subscribe(GeneralEvent.INFO, self._notify_info)
        self.event_bus.subscribe(GeneralEvent.DEBUG, self._notify_debug)


    def emit(self, event_type: GeneralEvent|EventBusEvent|MatchEvent|RobotEvent|PLCEvent|StateEvent|SwitchEvent|TeamEvent|UserAttentionEvent|TerminalEvent, data: dict = None):
        """
        Emit an event to the bus.
        """
        if data is None:
            data = {}
        if not isinstance(event_type, (GeneralEvent, EventBusEvent, MatchEvent, RobotEvent, PLCEvent, StateEvent, SwitchEvent, TeamEvent, UserAttentionEvent, TerminalEvent)):
            raise TypeError(f"Invalid event type: {type(event_type)}")
        if not isinstance(data, dict):
            raise TypeError(f"Data must be a dictionary, got {type(data)}")
        
        self.event_bus.emit(event_type, data)

    def _remote_shell_handler(self):
        # Should start an API to accept remote shell commands and track which things should be printed where.
        # This is a placeholder for the remote shell handler.
        self.emit(GeneralEvent.DEBUG, {"message": "Remote shell handler initialized"})

    def set_triggers(self, triggers: dict[str, Trigger]):
        self.triggers = triggers

    def getTrigger(self, name: str) -> Trigger | None:
        return self.triggers.get(name)
    
    def _check_triggers(self):
        for trigger in self.triggers.values():
            trigger.check(self)

    def _fms_main(self):
        while True:
            try:
                # If in a state, attach triggers and run execute loop
                if isinstance(self.mode, State):
                    self.mode.attach_triggers(self)
                    self.emit(GeneralEvent.DEBUG, {"message": f"Entered state: {self.mode.__class__.__name__}"})
                    self.emit(GeneralEvent.DEBUG, {"message": f"Attached triggers: {list(self.triggers.keys())}"})

                    while True:
                        # Check triggers
                        self._check_triggers()
                    
                        # Execute the current mode
                        result = self.mode.execute(self)

                        if result is not None:
                            last_mode = self.mode
                            self.mode = result
                            break

                # If in a transition, run execute and move to new state
                elif isinstance(self.mode, Transition):
                    self.emit(GeneralEvent.DEBUG, {"message": f"Executing transition: {self.mode.__class__.__name__}"})
                    result = self.mode.execute(last_mode, self)
                    if result is not None:
                        last_mode = self.mode
                        self.mode = result
                    else:
                        raise RuntimeError("Transition did not return a new state")

            except Exception as e:
                tb = traceback.format_exc()
                self.exception_queue.append((e, tb))
                self.emit(GeneralEvent.ERROR, {"message": f"Exception in FMS main loop: {e}, traceback: {tb}"})
                print(f"Exception in FMS main loop: {e}, traceback: {tb}")
                time.sleep(1)  # Prevent tight loop on exception


    def run(self):
        self._fms_main()


if __name__ == "__main__":
    fms = FMS()
    fms.run()