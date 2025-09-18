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
from utils.teams import TeamsManager, TeamData
from utils.user_attention import UserAttentionQueue # Possible future removal

from tools.terminal.shell_handler import ShellHandler, ShellInstance



class FMS:
    def __init__(self):
        # Exception queue for storing errors in (e, tb)
        self.exception_queue = []

        # Event bus for handling events
        self.event_bus = EventBus()
        threading.Thread(target=self.event_bus.run, daemon=True).start()
        self.emit(GeneralEvent.DEBUG, {"message": "Event bus initialized"})

        # User attention queue for handling things that need user attention; can be accessed via terminals or via web gui
        self.user_attention = UserAttentionQueue()
        self.emit(GeneralEvent.DEBUG, {"message": "User attention queue initialized"})

        # Create state store instance
        self.state_store = StateStore()
        self.emit(GeneralEvent.DEBUG, {"message": "State store initialized"})


    
    def _attach_subscribers(self):
        """
        Attach subscribers to the event bus.
        """
        ...


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


    
        
