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

    def _remote_shell_handler(self):
        # Should start an API to accept remote shell commands and track which things should be printed where.
        # This is a placeholder for the remote shell handler.
        self.emit(GeneralEvent.DEBUG, {"message": "Remote shell handler initialized"})

    def handle_null(self):
        # Error and ask if proceed to OFF, BOOTING, or CRASHED
        # Require field admin (FA) to confirm
        # Broadcast
        ...

    def handle_off(self):
        # Wait for "power up" (should be in front-end as a button)
        # Move to booting
        ...

    def handle_booting(self):
        # Connect to PLCs
        # Connect to switches and push primary config (all disallowed)
        # Start PLC servers
        # Connect to AP
        # Test connections
        # Move to modeless
        ...

    def handle_modeless(self):
        # Red/blue lights depending
        # Ask for where to move
        # Require FM to confirm
        # Displays should have year
        ...

    def handle_field_test(self):
        # API with all same light colors, indicators if e/a stops pressed, button for audio test, show statuses of switches/plcs and have options for testing
        # Move to modeless
        ...

    def handle_field_disabled(self):
        # Turn off lights
        # Turn off PLC servers
        # Push config to main switch to turn off POE for other switches, robot ap, and cut off DS nets
        # Only can move to field enabling
        ...

    def handle_field_enabling(self):
        # Turn on lights
        # Turn on PLC servers
        # Push config to main switch to turn on POE for devices and enable ds nets
        # Move to modeless
        # Requires FM
        ...

    def handle_field_presentation(self):
        # Turn lights to titans green
        # Set numbers to 3767
        # Also run field disabled code except for PLCs and side switch power
        # Requires FM
        ...

    def handle_field_development(self):
        # Allow full control, basically test but more control
        # Requires FA
        ...

    def handle_development_configuring(self):
        # Is pushing configs to switches and PLCs and AP
        ...

    def handle_development_main(self):
        # 
        ...

    def handle_development_estop(self):
        ...

    def handle_development_greenlight(self):
        ...

    def handle_testing_configuring(self):
        ...

    def handle_testing_main(self):
        ...

    def handle_testing_estop(self):
        ...

    def handle_testing_greenlight(self):
        ...

    def handle_match_configuring(self):
        ...

    def handle_match_pre(self):
        ...

    def handle_match_auto(self):
        ...
        
    def handle_match_transition(self):
        ...

    def handle_match_teleop(self):
        ...

    def handle_match_endgame(self):
        ...

    def handle_match_abort(self):
        ...

    def handle_match_post(self):
        ...

    def handle_match_greenlight(self):
        ...

    def handle_crashed(self):
        ...

    def handle_shutting_down(self):
        ...
