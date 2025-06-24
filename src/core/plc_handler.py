from enum import Enum
import requests
import logging


# logger = logging.getLogger("plc_handler")


class PLCHandler:
    """
    Class to handle communication with the PLC (Programmable Logic Controller). They are RPIs that run a webserver
    and can be controlled via HTTP requests.
    This class provides methods to set light colors, numbers, and retrieve E-Stop and A-Stop statuses for different stations.
    """
    class LightColor(Enum):
        """
        Enum to represent the different light colors that can be set on the PLC.
        """
        OFF = 0
        GREENLIGHT = 1 # green
        ESTOP = 2 # orange
        ASTOP = 3 # purple
        # Alliance colors
        RED = 4 # red alliance
        BLUE = 5 # blue alliance

    class Station(Enum):
        LEFT = 0
        CENTER = 1
        RIGHT = 2
        FIELD = 0


    def __init__(self, fms, ip:str, username:str = "plc", password:str = "c0sm0splc"):
        """
        Initialize the PLCHandler with the PLC's IP address.
        """
        self.fms = fms
        self.ip = str(ip)
        self.username = username
        self.password = password

    def start_remote_server(self):
        """
        Using SSH, start the remote server on the PLC.
        """
        ...


    def set_light_color(self, station:Station, color:LightColor):
        """
        Set the light color for a specific station on the PLC.
        :param station: The station to set the light color for.
        :param color: The color to set the light to.
        """
        # Implementation to set the light color on the PLC
        endpoint = f"http://{self.ip}/set_light_color/{station.value}"
        # Example implementation using requests library
        try:
            response = requests.post(endpoint, json={"color": color.value})
            response.raise_for_status()  # Raise an error for bad responses
            self.fms.event_bus.emit("plc_light_set", {
                "station": station.name,
                "color": color.name
            })
        except requests.RequestException as e:
            # logger.error(f"Failed to set light color for station {station.name} to {color.name}: {e}")
            self.fms.event_bus.emit("plc_error", {
                "station": station.name,
                "color": color.name,
                "error": str(e)
            })
            raise

    def set_light_color_alliance(self, color:LightColor):
        self.set_light_color(self.Station.LEFT, color)
        self.set_light_color(self.Station.CENTER, color)
        self.set_light_color(self.Station.RIGHT, color)

    def set_number(self, station:Station, number:int):
        """
        Set the number on the PLC for a specific station.
        :param station: The station to set the number for.
        :param number: The team number to set on the PLC.
        """
        # Implementation to set the number on the PLC
        endpoint = f"http://{self.ip}/set_number/{station.value}"
        # Example implementation using requests library
        try:
            response = requests.post(endpoint, json={"number": number})
            response.raise_for_status()  # Raise an error for bad responses
        except requests.RequestException as e:
            # logger.error(f"Failed to set number for station {station.name} for team number {number}: {e}")
            self.fms.event_bus.emit("plc_number_error", {
                "station": station.name,
                "error": str(e)
            })
            raise

    def get_estop(self, station:Station) -> bool:
        """
        Get the E-Stop status for a specific station.
        :param station: The station to get the E-Stop status for.
        :return: True if E-Stop is active, False otherwise.
        """
        # Implementation to get the E-Stop status from the PLC
        endpoint = f"http://{self.ip}/get_estop/{station.value}"
        try:
            response = requests.get(endpoint)
            response.raise_for_status()  # Raise an error for bad responses
            return response.json().get("estop", False)  # Assuming the PLC returns a JSON with "estop" key
        except requests.RequestException as e:
            # logger.error(f"Failed to get E-Stop status for station {station.name}: {e}")
            self.fms.event_bus.emit("error", {
                "error": f"Failed to get E-Stop status for station {station.name}: {e}"
            })
            raise

    def get_astop(self, station:Station) -> bool:
        """
        Get the A-Stop status for a specific station.
        :param station: The station to get the A-Stop status for.
        :return: True if A-Stop is active, False otherwise.
        """
        # Implementation to get the A-Stop status from the PLC
        endpoint = f"http://{self.ip}/get_astop/{station.value}"
        try:
            response = requests.get(endpoint)
            response.raise_for_status()  # Raise an error for bad responses
            return response.json().get("astop", False)  # Assuming the PLC returns a JSON with "astop" key
        except requests.RequestException as e:
            logger.error(f"Failed to get A-Stop status for station {station.name}: {e}")
            raise

    def get_estops(self) -> list:
        """
        Get the E-Stop status for all stations.
        :return: A list of E-Stop statuses for each station.
        """
        return [self.get_estop(station) for station in self.Station]

    def get_astops(self) -> list:
        """
        Get the A-Stop status for all stations.
        :return: A list of A-Stop statuses for each station.
        """
        return [self.get_astop(station) for station in self.Station]