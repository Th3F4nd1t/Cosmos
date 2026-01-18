
from enum import Enum
from typing import Any, List
from network.ds_net import Station


class RobotState(Enum):
    DISABLED = 0
    AUTO = 1
    TELEOP = 2
    TEST = 3

class MatchType(Enum):
    TEST = "test"
    PRACTICE = "practice"
    QUALIFICATION = "qualification"
    PLAYOFF = "playoff"

class TeamData:
    def __init__(self, number:int = None, name:str = None, ip:str = None,
                 ds_connected:bool = None, radio_connected:bool = None,
                 rio_connected:bool = None, state:RobotState = None,
                 estop:bool = None, astop:bool = None, enabled:bool = None):
        
        self.number:int = number
        self.name:str = name
        self.ip:str = ip
        self.ds_connected:bool = ds_connected
        self.radio_connected:bool = radio_connected
        self.rio_connected:bool = rio_connected
        self.state:RobotState = state
        self.estop:bool = estop
        self.astop:bool = astop
        self.enabled:bool = enabled

    def get(self):
        if (isinstance(self.number, int) and
            isinstance(self.name, str) and
            isinstance(self.ip, str) and
            isinstance(self.ds_connected, bool) and
            isinstance(self.radio_connected, bool) and
            isinstance(self.rio_connected, bool) and
            isinstance(self.state, RobotState) and
            isinstance(self.estop, bool) and
            isinstance(self.astop, bool) and
            isinstance(self.enabled, bool)):
            return {
                "number": self.number,
                "name": self.name,
                "ip": self.ip,
                "status" : {
                    "ds_connected": self.ds_connected,
                    "radio_connected": self.radio_connected,
                    "rio_connected": self.rio_connected,
                    "state": self.state,
                    "estop": self.estop,
                    "astop": self.astop,
                    "enabled": self.enabled
                }
            }
        return None

    def load(self, dicti:dict):
        self.number = dicti["number"] if dicti["number"] is not None else 0
        self.name = dicti["name"] if dicti["name"] is not None else "No Name Provided"
        self.ip = dicti["ip"] # Doesn't matter if it's None
        self.ds_connected = dicti["status"]["ds_connected"] if dicti["status"]["ds_connected"] is not None else False
        self.radio_connected = dicti["status"]["radio_connected"] if dicti["status"]["radio_connected"] is not None else False
        self.rio_connected = dicti["status"]["rio_connected"] if dicti["status"]["rio_connected"] is not None else False
        self.state = RobotState[dicti["status"]["state"].upper()] if dicti["status"]["state"] is not None else RobotState.DISABLED
        self.estop = dicti["status"]["estop"] if dicti["status"]["estop"] is not None else False
        self.astop = dicti["status"]["astop"] if dicti["status"]["astop"] is not None else False
        self.enabled = dicti["status"]["enabled"] if dicti["status"]["enabled"] is not None else False


class StateStore:
    def __init__(self):
        self.state:dict[str, Any] = {
            "running" : True, # False will force stop the FMS. NOT RECOMMENDED
            "teams" : [
                TeamData(
                    number=1,
                    name="Test Team",
                    ip="10.0.1.5",
                    ds_connected=False,
                    radio_connected=False,
                    rio_connected=False,
                    state=RobotState.DISABLED,
                    estop=False,
                    astop=False,
                    enabled=False
                ),
                TeamData(
                    number=2,
                    name="Test Team 2",
                    ip="10.0.2.5",
                    ds_connected=False,
                    radio_connected=False,
                    rio_connected=False,
                    state=RobotState.DISABLED,
                    estop=False,
                    astop=False,
                    enabled=False
                ),
                TeamData(
                    number=3,
                    name="Test Team 3",
                    ip="10.0.3.5",
                    ds_connected=False,
                    radio_connected=False,
                    rio_connected=False,
                    state=RobotState.DISABLED,
                    estop=False,
                    astop=False,
                    enabled=False
                ),
                TeamData(
                    number=4,
                    name="Test Team 4",
                    ip="10.0.4.5",
                    ds_connected=False,
                    radio_connected=False,
                    rio_connected=False,
                    state=RobotState.DISABLED,
                    estop=False,
                    astop=False,
                    enabled=False
                ),
                TeamData(
                    number=5,
                    name="Test Team 5",
                    ip="10.0.5.5",
                    ds_connected=False,
                    radio_connected=False,
                    rio_connected=False,
                    state=RobotState.DISABLED,
                    estop=False,
                    astop=False,
                    enabled=False
                ),
                TeamData(
                    number=6,
                    name="Test Team 6",
                    ip="10.0.6.5",
                    ds_connected=False,
                    radio_connected=False,
                    rio_connected=False,
                    state=RobotState.DISABLED,
                    estop=False,
                    astop=False,
                    enabled=False
                )
            ],
            "match" : {
                "number" : 0,
                "repeat" : 0,
                "type" : MatchType.TEST, # test, practice, qualification, playoff
                "time_left" : -1,
            }
        }
        
    
    def set_running(self, running: bool):
        """
        Set whether the FMS is running or not.
        """
        if not isinstance(running, bool):
            raise TypeError(f"Setting running bool of state store, expected boolean, got {type(running)}")
        
        self.state["running"] = running

    def is_running(self) -> bool:
        """
        Check if the FMS is running.
        """
        return self.state["running"]
    
    def set_team_number(self, station:Station, number:int):
        """
        Set the team number for a given station.
        """
        if not isinstance(station, Station):
            raise TypeError(f"Setting team number in state store, expected Station enum, got {type(station)}")
        
        if not isinstance(number, int):
            raise TypeError(f"Setting team number in state store, expected int, got {type(number)}")
        
        self.state["teams"][station.value].number = number
    
    def get_team_number(self, station:Station) -> int:
        """
        Get the team number for a given station.
        """
        if not isinstance(station, Station):
            raise TypeError(f"Getting team number from state store, expected Station enum, got {type(station)}")
        
        return self.state["teams"][station.value].number
    
    def set_team_name(self, station:Station, name:str):
        """
        Set the team name for a given station.
        """
        if not isinstance(station, Station):
            raise TypeError(f"Setting team name in state store, expected Station enum, got {type(station)}")
        
        if not isinstance(name, str):
            raise TypeError(f"Setting team name in state store, expected str, got {type(name)}")
        
        self.state["teams"][station.value].name = name

    def get_team_name(self, station:Station) -> str:
        """
        Get the team name for a given station.
        """
        if not isinstance(station, Station):
            raise TypeError(f"Getting team name from state store, expected Station enum, got {type(station)}")
        
        return self.state["teams"][station.value].name
    
    def set_team_ip(self, station:Station, ip:str):
        """
        Set the team IP for a given station.
        """
        if not isinstance(station, Station):
            raise TypeError(f"Setting team IP in state store, expected Station enum, got {type(station)}")
        
        if not isinstance(ip, str):
            raise TypeError(f"Setting team IP in state store, expected str, got {type(ip)}")
        
        self.state["teams"][station.value].ip = ip

    def get_team_ip(self, station:Station) -> str:
        """
        Get the team IP for a given station.
        """
        if not isinstance(station, Station):
            raise TypeError(f"Getting team IP from state store, expected Station enum, got {type(station)}")
        
        return self.state["teams"][station.value].ip
    
    def set_team_ds_connected(self, station:Station, ds_connected:bool):
        """
        Set whether the team at a given station is connected to the DS.
        """
        if not isinstance(station, Station):
            raise TypeError(f"Setting team DS connected in state store, expected Station enum, got {type(station)}")
        
        if not isinstance(ds_connected, bool):
            raise TypeError(f"Setting team DS connected in state store, expected bool, got {type(ds_connected)}")
        
        self.state["teams"][station.value].ds_connected = ds_connected

    def get_team_ds_connected(self, station:Station) -> bool:
        """
        Get whether the team at a given station is connected to the DS.
        """
        if not isinstance(station, Station):
            raise TypeError(f"Getting team DS connected from state store, expected Station enum, got {type(station)}")
        
        return self.state["teams"][station.value].ds_connected
    
    def set_team_radio_connected(self, station:Station, radio_connected:bool):
        """
        Set whether the team at a given station is connected to the radio.
        """
        if not isinstance(station, Station):
            raise TypeError(f"Setting team radio connected in state store, expected Station enum, got {type(station)}")
        
        if not isinstance(radio_connected, bool):
            raise TypeError(f"Setting team radio connected in state store, expected bool, got {type(radio_connected)}")
        
        self.state["teams"][station.value].radio_connected = radio_connected

    def get_team_radio_connected(self, station:Station) -> bool:
        """
        Get whether the team at a given station is connected to the radio.
        """
        if not isinstance(station, Station):
            raise TypeError(f"Getting team radio connected from state store, expected Station enum, got {type(station)}")
        
        return self.state["teams"][station.value].radio_connected
    
    def set_team_rio_connected(self, station:Station, rio_connected:bool):
        """
        Set whether the team at a given station is connected to the RIO.
        """
        if not isinstance(station, Station):
            raise TypeError(f"Setting team RIO connected in state store, expected Station enum, got {type(station)}")
        
        if not isinstance(rio_connected, bool):
            raise TypeError(f"Setting team RIO connected in state store, expected bool, got {type(rio_connected)}")
        
        self.state["teams"][station.value].rio_connected = rio_connected

    def get_team_rio_connected(self, station:Station) -> bool:
        """
        Get whether the team at a given station is connected to the RIO.
        """
        if not isinstance(station, Station):
            raise TypeError(f"Getting team RIO connected from state store, expected Station enum, got {type(station)}")
        
        return self.state["teams"][station.value].rio_connected
    
    def set_team_state(self, station:Station, state:RobotState):
        """
        Set the state of the robot at a given station.
        """
        if not isinstance(station, Station):
            raise TypeError(f"Setting team state in state store, expected Station enum, got {type(station)}")
        
        if not isinstance(state, RobotState):
            raise TypeError(f"Setting team state in state store, expected RobotState enum, got {type(state)}")
        
        self.state["teams"][station.value].state = state

    def get_team_state(self, station:Station) -> RobotState:
        """
        Get the state of the robot at a given station.
        """
        if not isinstance(station, Station):
            raise TypeError(f"Getting team state from state store, expected Station enum, got {type(station)}")

        return self.state["teams"][station.value].state
    
    def set_team_estop(self, station:Station, estop:bool):
        """
        Set whether the team at a given station is in E-Stop.
        """
        if not isinstance(station, Station):
            raise TypeError(f"Setting team E-Stop in state store, expected Station enum, got {type(station)}")
        
        if not isinstance(estop, bool):
            raise TypeError(f"Setting team E-Stop in state store, expected bool, got {type(estop)}")
        
        self.state["teams"][station.value].estop = estop

    def get_team_estop(self, station:Station) -> bool:
        """
        Get whether the team at a given station is in E-Stop.
        """
        if not isinstance(station, Station):
            raise TypeError(f"Getting team E-Stop from state store, expected Station enum, got {type(station)}")
        
        return self.state["teams"][station.value].estop
    
    def set_team_astop(self, station:Station, astop:bool):
        """
        Set whether the team at a given station is in A-Stop.
        """
        if not isinstance(station, Station):
            raise TypeError(f"Setting team A-Stop in state store, expected Station enum, got {type(station)}")
        
        if not isinstance(astop, bool):
            raise TypeError(f"Setting team A-Stop in state store, expected bool, got {type(astop)}")
        
        self.state["teams"][station.value].astop = astop

    def get_team_astop(self, station:Station) -> bool:
        """
        Get whether the team at a given station is in A-Stop.
        """
        if not isinstance(station, Station):
            raise TypeError(f"Getting team A-Stop from state store, expected Station enum, got {type(station)}")
        
        return self.state["teams"][station.value].astop
    
    def set_team_enabled(self, station:Station, enabled:bool):
        """
        Set whether the team at a given station is enabled.
        """
        if not isinstance(station, Station):
            raise TypeError(f"Setting team enabled in state store, expected Station enum, got {type(station)}")
        
        if not isinstance(enabled, bool):
            raise TypeError(f"Setting team enabled in state store, expected bool, got {type(enabled)}")
        
        self.state["teams"][station.value].enabled = enabled

    def get_team_enabled(self, station:Station) -> bool:
        """
        Get whether the team at a given station is enabled.
        """
        if not isinstance(station, Station):
            raise TypeError(f"Getting team enabled from state store, expected Station enum, got {type(station)}")
        
        return self.state["teams"][station.value].enabled
    
    def get_teams(self) -> List[TeamData]:
        """
        Get the list of teams.
        """
        return self.state["teams"]
    
    def set_match_number(self, number:int):
        """
        Set the current match number.
        """
        if not isinstance(number, int):
            raise TypeError(f"Setting match number in state store, expected int, got {type(number)}")

        self.state["match"]["number"] = number

    def get_match_number(self) -> int:
        """
        Get the current match number.
        """
        return self.state["match"]["number"]
        
        self.state["match"]["number"] = number

    def set_match_repeat(self, repeat:int):
        """
        Set the current match repeat number.
        """
        if not isinstance(repeat, int):
            raise TypeError(f"Setting match repeat in state store, expected int, got {type(repeat)}")

        self.state["match"]["repeat"] = repeat

    def get_match_repeat(self) -> int:
        """
        Get the current match repeat number.
        """
        return self.state["match"]["repeat"]
    
    def set_match_type(self, match_type:MatchType):
        """
        Set the current match type.
        """
        if not isinstance(match_type, MatchType):
            raise TypeError(f"Setting match type in state store, expected MatchType enum, got {type(match_type)}")

        self.state["match"]["type"] = match_type

    def get_match_type(self) -> MatchType:
        """
        Get the current match type.
        """
        return self.state["match"]["type"]
    
    def set_match_time_left(self, time_left:int):
        """
        Set the time left in the current match.
        """
        if not isinstance(time_left, int):
            raise TypeError(f"Setting match time left in state store, expected int, got {type(time_left)}")
        
        self.state["match"]["time_left"] = time_left

    def get_match_time_left(self) -> int:
        """
        Get the time left in the current match.
        """
        return self.state["match"]["time_left"]

    def get(self) -> dict:
        """
        Get the current state of the FMS.
        """
        return self.state