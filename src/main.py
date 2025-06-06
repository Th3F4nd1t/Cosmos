# Load config.yaml (utils/config_loader.py)
import logging
import threading
import time
import traceback
# from flask import Flask, request

from core.event_bus import EventBus
from core.match_controller import MatchController
from core.state_store import StateStore, States
from core.plc_handler import PLCHandler
from utils import driverstation_ip
from utils.config_loader import load_config
from utils.user_attention import UserAttentionQueue
# Start station managers, PLC  handler, etc
# Launch networkhandler
# launch api server

logger = logging.getLogger("fms")
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class FMS:
    def __init__(self):
        # load config.yaml
        # self.config = load_config("config.yaml")

        self.exception_queue = []

        # init event bus
        self.event_bus = EventBus()
        threading.Thread(target=self.event_bus.run, daemon=True).start()

        # create user attention queue
        self.user_attention = UserAttentionQueue()

        # spawn console user attention handler
        self._user_attention_thread = threading.Thread(target=self._user_attention_handler, daemon=True)
        self._user_attention_thread.start()

        # create state store
        self.state_store = StateStore()

        # spawn state handler
        self._state_handler_thread = threading.Thread(target=self.state_handler, daemon=True)
        self._state_handler_thread.start()

        # Start web server
        # self._web_server_thread = threading.Thread(target=self._web_server, daemon=True)
        # self._web_server_thread.start()


    # def _web_server(self):
    #     # flask API server
    #     app = Flask("COSMOS-API")

    #     # TODO: make api, no ui, with authentication

    #     app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)

    def _user_attention_handler(self):
        while True:
            item:tuple[str, list[str], int, int] | None = self.user_attention.get()
            if item is not None:

                if item[1] is not None: # options are provided
                    print(f"User attention: {item[0]}")
                    for i, option in enumerate(item[1]):
                        print(f"{i}: {option}")
                    response = input("Select an option: ")
                    try:
                        response = int(response)
                        if response < 0 or response >= len(item[1]):
                            raise ValueError
                    except ValueError:
                        print("Invalid response, please try again.")
                        continue

                else: # no options provided, text input
                    response = input(f"User attention: {item[0]}")

                self.user_attention.set_response(item[2],response)


    def state_handler(self):
        while True:
            try:
                match self.state_store.get_state():
                    case States.NULL:
                        ...
                        # Error and ask if proceed to OFF, BOOTING, or CRASHED
                        logger.error("State is NULL")
                        idn = self.user_attention.add("State is NULL, please select a state to proceed", ["OFF", "BOOTING", "CRASHED"])
                        # Wait for user attention to respond
                        while self.user_attention.get(idn)[3] is None: continue

                        match self.user_attention.get(idn)[3]:
                            case 0:
                                self.state_store.set_state(States.OFF)
                            case 1:
                                self.state_store.set_state(States.BOOTING)
                            case 2:
                                self.state_store.set_state(States.CRASHED)
                        
                        logger.info(f"Proceeding to {self.state_store.get_state()}")
                        self.user_attention.remove(idn)

                    case States.OFF:
                        idn = self.user_attention.add("Turn on the system?", ["Yes", "No"])
                        # Wait for user attention to respond
                        while self.user_attention.get(idn)[3] is None: continue
                        
                        match self.user_attention.get(idn)[3]:
                            case 0:
                                self.state_store.set_state(States.BOOTING)
                                logger.info("State is OFF, proceeding to BOOTING")
                                self.user_attention.remove(idn)
                            case 1:
                                # Do nothing, stay in OFF state
                                logger.info("State is OFF, staying in OFF")
                                self.user_attention.remove(idn)
                                continue
                            case _:
                                # Invalid response, stay in OFF state
                                logger.error("Invalid response, staying in OFF")
                                self.user_attention.remove(idn)
                                continue

                    case States.BOOTING:
                        # Setup thingies.
                        self.main_plc = PLCHandler("10.0.100.200")
                        self.red_plc = PLCHandler("10.0.100.210")
                        self.blue_plc = PLCHandler("10.0.100.220")
                        # Connect to main switch and push first config
                        # Connect to red switch and push first config
                        # Connect to blue switch and push first config

                        # Start PLC servers
                        self.main_plc.start_remote_server()
                        self.red_plc.start_remote_server()
                        self.blue_plc.start_remote_server()
                        
                        # Connect to AP

                        # test connections
                        self.main_plc.get_estops()
                        self.red_plc.get_estops()
                        self.blue_plc.get_estops()

                        self.state_store.set_state(States.MODELESS)

                    case States.MODELESS:
                        self.red_plc.set_light_color_alliance(PLCHandler.LightColor.RED)
                        self.blue_plc.set_light_color_alliance(PLCHandler.LightColor.BLUE)

                        # ask for next state
                        idn = self.user_attention.add("MODELESS, to where?", ["field-test", "field-disabled", "field-presentation", "field-development", "field-diagnostic", "development-configuring", "testing-configuring", "match-configuring", "shutting-down"])
                        
                        # Wait for user attention to respond
                        while self.user_attention.get(idn)[3] is None: continue
                        
                        match self.user_attention.get(idn)[3]:
                            case 0: self.state_store.set_state(States.FIELD_TEST)
                            case 1: self.state_store.set_state(States.FIELD_DISABLED)
                            case 2: self.state_store.set_state(States.FIELD_PRESENTATION)
                            case 3: self.state_store.set_state(States.FIELD_DEVELOPMENT)
                            case 4: self.state_store.set_state(States.FIELD_DIAGNOSTIC)
                            case 5: self.state_store.set_state(States.DEVELOPMENT_CONFIGURING)
                            case 6: self.state_store.set_state(States.TESTING_CONFIGURING)
                            case 7: self.state_store.set_state(States.MATCH_CONFIGURING)
                            case 8: self.state_store.set_state(States.SHUTTING_DOWN)

                        logger.info(f"Proceeding to {self.state_store.get_state()}")
                        self.user_attention.remove(idn)

                    case States.FIELD_TEST:
                        # wait for all estops to be pushed
                        while not (all(self.main_plc.get_estop(PLCHandler.Station.FIELD).values()) and
                                    all(self.red_plc.get_estops().values()) and
                                    all(self.blue_plc.get_estops().values())):
                            time.sleep(1)

                        # wait for all a-stops to be pushed
                        while not (all(self.red_plc.get_astops().values()) and
                                    all(self.blue_plc.get_astops().values())):
                            time.sleep(1)

                        # turn lights all colors
                        for color in PLCHandler.LightColor:
                            self.red_plc.set_light_color_alliance(color)
                            self.blue_plc.set_light_color_alliance(color)

                            idn = self.user_attention.add("Next light color?", ["y"])
                            # Wait for user attention to respond
                            while self.user_attention.get(idn)[3] is None: continue
                            self.user_attention.remove(idn)

                        # set team numbers
                        self.main_plc.set_number(PLCHandler.Station.FIELD, 1)
                        self.red_plc.set_number(PLCHandler.Station.FIELD, 2)
                        self.blue_plc.set_number(PLCHandler.Station.FIELD, 3)
                        # test audio
                        # test AP?
                        ...

                    case States.FIELD_DISABLED:
                        # Turn all lights off
                        # Turn off PLC servers
                        # Push config to main switch to disable POE to robot AP, and to cut off connection from DS
                        ...
                    
                    case States.FIELD_PRESENTATION:
                        # Turn all lights to a set color
                        # Disable all robots
                        # Push config to main switch to disable POE to robot AP, and to cut off connection from DS
                        ...
                    
                    case States.FIELD_DEVELOPMENT:
                        # Allow full control of all field aspects to the API
                        # Enable development sites on the webserver
                        ...
                    
                    case States.FIELD_DIAGNOSTIC:
                        # Allow full control of all field aspects to the API
                        # Enable diagnostic sites on the webserver
                        ...
                    
                    case States.DEVELOPMENT_CONFIGURING:
                        # Ask for teams
                        # setup teams in state store
                        # set switch configs
                        # set PLC configs
                        # set AP configs
                        # enable public log viewing
                        # enable robot development sites on the webserver
                        # enable robot diagnostic sites on the webserver
                        ...
                    
                    case States.DEVELOPMENT_MAIN:
                        # allow robots to be enabled and disable via website, along with auto runnning, etc.
                        # lights are set to red/blue depending on the robot
                        ...
                    
                    case States.DEVELOPMENT_ESTOP:
                        # estops all robots, not just the one teams
                        # turn lights orange
                        ...
                    
                    case States.DEVELOPMENT_GREENLIGHT:
                        # disable all robots
                        # turn lights green
                        ...
                    
                    case States.TESTING_CONFIGURING:
                        # Ask for teams
                        # setup teams in state store
                        # set switch configs
                        # set PLC configs
                        # set AP configs
                        # enable public log viewing
                        # enable robot testing sites on the webserver
                        # enable robot diagnostic sites on the webserver
                        ...

                    case States.TESTING_MAIN:
                        # allow robots to be enabled and disable via website, along with auto runnning, etc.
                        # lights are set to red/blue depending on the robot
                        ...

                    case States.TESTING_ESTOP:
                        # estops all robots, not just the one teams
                        # turn lights orange
                        ...

                    case States.TESTING_GREENLIGHT:
                        # disable all robots
                        # turn lights green
                        ...
                    
                    case States.MATCH_CONFIGURING:
                        # ask for teams and confirm match number (which should be incremented)
                        self.state_store.state["match"]["number"] += 1
                        teams_id = self.user_attention.add("Enter teams (comma separated - r1 r2 r3 b1 b2 b3):")
                        match_number_id = self.user_attention.add(f"Match number (blank for {self.state_store.state['match']['number']}): ")
                        
                        # Wait for user attention to respond
                        while self.user_attention.get(teams_id)[3] is None or self.user_attention.get(match_number_id)[3] is None: continue
                        
                        teams = self.user_attention.get(teams_id)[3]
                        match_number = self.user_attention.get(match_number_id)[3]

                        # clean up
                        self.user_attention.remove(teams_id)
                        self.user_attention.remove(match_number_id)
                        
                        if match_number != "":
                            self.state_store.state["match"]["number"] = int(match_number)

                        teams = teams.split(",")
                        teams = [team.strip() for team in teams]
                        if len(teams) != 6:
                            logger.error("Invalid number of teams, must be 6")
                            self.state_store.state["match"]["number"] -= 1
                            self.state_store.set_state(States.MATCH_CONFIGURING)
                            continue

                        # setup teams in state store
                        self.state_store.state["teams"] = {}
                        for team in teams:
                            self.state_store.state["teams"][team] = {
                                "ip" : driverstation_ip.driverstation_ip(team),
                                "status" : {
                                    "ds_connected" : False,
                                    "radio_connected" : False,
                                    "rio_connected" : False,
                                    "state" : "disabled", # disabled, auto, teleop
                                    "estop" : False,
                                    "astop" : False
                                }
                            }

                        # TODO: setup match, configure switches, lights, etc.

                        # Move to MATCH_PRE
                        logger.info(f"Match configuration complete; proceeding to MATCH_PRE with teams: {self.state_store.state['teams'].keys()}")
                        self.state_store.set_state(States.MATCH_PRE)

                    
                    case States.MATCH_PRE:
                        match_controller = MatchController(self)
                        
                        idn = self.user_attention.add("Match is in pre-match, start match?", ["Yes", "No"])
                        # Wait for user attention to respond
                        while self.user_attention.get(idn)[3] is None: continue

                        match self.user_attention.get(idn)[3]:
                            case 0:
                                match_controller.start_match()
                                logger.info("State is MATCH_PRE, proceeding to MATCH_AUTONOMOUS")
                                self.user_attention.remove(idn)
                            case 1:
                                # Do nothing, stay in MATCH_PRE state
                                logger.info("State is MATCH_PRE, staying in MATCH_PRE")
                                self.user_attention.remove(idn)
                                continue
                            case _:
                                # Invalid response, stay in MATCH_PRE state
                                logger.error("Invalid response, staying in MATCH_PRE")
                                self.user_attention.remove(idn)
                                continue
                    
                    case States.MATCH_AUTONOMOUS:
                        ...
                    
                    case States.MATCH_TRANSITION:
                        ...
                    
                    case States.MATCH_TELEOP:
                        ...
                    
                    case States.MATCH_ENDGAME:
                        ...
                    
                    case States.MATCH_ABORT_OR_ESTOP:
                        ...
                    
                    case States.MATCH_POST:
                        ...
                    
                    case States.MATCH_GREENLIGHT:
                        # TODO: field good logic

                        # modeless or another match
                        idn = self.user_attention.add("Greenlight received, to where?", ["MODELESS", "MATCH_CONFIGURING"])
                        # Wait for user attention to respond
                        while self.user_attention.get(idn)[3] is None: continue
                        match self.user_attention.get(idn)[3]:
                            case 0:
                                self.state_store.set_state(States.MODELESS)
                            case 1:
                                self.state_store.set_state(States.MATCH_CONFIGURING)
                        logger.info(f"Proceeding to {self.state_store.get_state()}")
                        self.user_attention.remove(idn)
                    
                    case States.CRASHED:
                        # Show error message and traceback from exception queue
                        if self.exception_queue:
                            for i in range(len(self.exception_queue)):
                                e, tb = self.exception_queue.pop()
                                logger.error(f"Exception: {e}")
                                logger.error(f"Traceback: {tb}")
                        else:
                            logger.error("No exception in queue")

                        # proceed to OFF or SHUTTING_DOWN (recommended)
                        idn = self.user_attention.add("FMS CRASHED", ["OFF", "SHUTTING_DOWN - recommended"])

                        while self.user_attention.get(idn)[3] is None: continue
                        match self.user_attention.get(idn)[3]:
                            case 0:
                                self.state_store.set_state(States.OFF)
                            case 1:
                                self.state_store.set_state(States.SHUTTING_DOWN)
                        logger.info(f"Proceeding to {self.state_store.get_state()}")
                        self.user_attention.remove(idn)
                    
                    case States.SHUTTING_DOWN:
                        # TODO: shutdown sequence
                        logger.info("Shutting down...")
                        self.state_store.set_state(States.OFF)

            except Exception as e:
                self.exception_queue.insert(0, (e, str(e.__traceback__)))
                self.state_store.set_state(States.CRASHED)
                logger.error("State handler crashed, setting state to CRASHED")


if __name__ == "__main__":
    try:
        fms = FMS()
        # Keep alive
        while True:
            pass
    except KeyboardInterrupt:
        logger.info("Oh sure, just Ctrl+C out of your responsibilities. Real mature.")
    except Exception as e:
        logger.critical("---- HOLY COW WHAT DID YOU DO? ----")
        tb_text = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
        logger.critical(f"Exception:\n{tb_text}")
        logger.critical("This is beyond duct tape, prayers, and caffeine. Pack it up, go home, and reconsider your life choices.")
