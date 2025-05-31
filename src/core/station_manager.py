from enum import Enum

# from utils.driverstation_ip import driverstation_ip
from main import FMS


class StationManager:
    """
    Class to manage the driver stations, robot states, and their respective tasks.
    """
    class Station(Enum):
        RED_1 = 1
        RED_2 = 2
        RED_3 = 3
        BLUE_1 = 4
        BLUE_2 = 5
        BLUE_3 = 6

    def __init__(self, fms:FMS, station_id:Station, team_number: int):
        """
        Initialize the StationManager with a station ID and team number.
        """
        self.fms = fms
        self.station_id = station_id
        self.team_number = team_number
        
    def _send_udp_update(self):
        """
        Send an update to the driver station via UDP.
        """
        # self.fms.network_handler.send_udp
        ...