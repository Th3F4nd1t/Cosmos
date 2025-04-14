import datetime
from enum import Enum
import threading
import time
from scapy.all import Ether, Dot1Q, IP, UDP, sendp
import socket

from ds import DriverStation, AllianceStation, DriverStationMode

# https://frcture.readthedocs.io/en/latest/driverstation/fms_to_ds.html

class ArenaMode(Enum):
    TEST = 0
    PRACTICE_MATCH = 1
    QUAL_MATCH = 2
    PLAYOFF_MATCH = 3
    DEVELOPMENT = 4
    NO_FMS = 5


class Arena:
    def __init__(self):
        self.driverstations = {
            "object" : [
                DriverStation(3886, AllianceStation.RED1),
                DriverStation(6, AllianceStation.RED2),
                DriverStation(None, AllianceStation.RED3),
                DriverStation(None, AllianceStation.BLUE1),
                DriverStation(None, AllianceStation.BLUE2),
                DriverStation(None, AllianceStation.BLUE3)
            ],
            "number" : [
                None,
                None,
                None,
                None,
                None,
                None
            ],
            "sockets" : [
                socket.socket(socket.AF_INET, socket.SOCK_DGRAM),
                socket.socket(socket.AF_INET, socket.SOCK_DGRAM),
                socket.socket(socket.AF_INET, socket.SOCK_DGRAM),
                socket.socket(socket.AF_INET, socket.SOCK_DGRAM),
                socket.socket(socket.AF_INET, socket.SOCK_DGRAM),
                socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            ]
            
        }

        self.field = {
            "mode" : ArenaMode.TEST,
            "match_number" : 1,
            "time_left" : 130,
            "isEstop" : False,
        }

        self.udp_send_port = 1120
        self.udp_tods_running = True

    def log(self, message: str, level: str = "INFO"):
        levels = {
            "INFO": "\033[94m",
            "WARNING": "\033[93m",
            "ERROR": "\033[91m",
            "DEBUG": "\033[92m"
        }
        reset = "\033[0m"
        print(f"{levels.get(level, reset)}[{level}] {reset}{message}")
    
    def start_udp_thread(self):
        def loop():
            while self.udp_tods_running:
                try:
                    for ds in self.driverstations["object"]:
                        ds.send_udp(self)
                except Exception as e:
                    self.log(f"Error sending UDP packet: {e}", "ERROR")
                    self.log(f"Stopping UDP thread", "ERROR")
                    self.udp_tods_running = False
                finally:
                    self.close_sockets()

                time.sleep(0.5) # 500ms

        thread = threading.Thread(target=loop, daemon=True)
        thread.start()
        self.log("UDP thread started", "INFO")

    def end_udp_thread(self):
        self.udp_tods_running = False
        self.log("UDP thread stopped", "INFO")

    def run_match(self, mode: ArenaMode, match_number: int, auton_time: int = 15, teleop_time: int = 120):
        self.log(f"Starting pre-match for match {match_number}", "INFO")
        self.field["mode"] = mode
        self.field["match_number"] = match_number
        self.field["time_left"] = auton_time + teleop_time
        if not self.udp_tods_running:
            self.log("UDP to driverstations thread not running, starting it", "INFO")
            self.start_udp_thread()

        for ds in self.driverstations["object"]:
            ds.isEstop = False
            ds.isAstop = False
            ds.isEnabled = False
            ds.mode = DriverStationMode.AUTO

        self.log("Pre-match done", "INFO")

        if input("'start' to start the match: ") == "start":
            self.log("Starting match", "INFO")
        else:
            self.log("Match aborted", "INFO")
            return
        
        start_time = time.time()
        end_time = start_time + self.field["time_left"]
        
        # Run thru auto
        self.log("Running auto", "INFO")
        for ds in self.driverstations["object"]:
            ds.isEnabled = True
        
        while True:
            time_left = end_time - time.time()
            self.field["time_left"] = time_left
            if self.field["isEstop"]:
                self.log("Match E-Stopped", "INFO")
                for ds in self.driverstations["object"]:
                    ds.isEnabled = False
                    ds.isEstop = True
                break
            if time_left <= end_time - auton_time:
                break

        if not self.field["isEstop"]:

            self.log("Auto time expired, switching to teleop", "INFO")

            for ds in self.driverstations["object"]:
                ds.isEnabled = False
                ds.mode = DriverStationMode.TELEOP

            time.sleep(1) # 1 second delay to allow for teleop mode to be set
            self.log("Running teleop", "INFO")

            for ds in self.driverstations["object"]:
                ds.isEnabled = True

            while True:
                time_left = end_time - time.time()
                self.field["time_left"] = time_left
                if self.field["isEstop"]:
                    self.log("Match E-Stopped", "INFO")
                    for ds in self.driverstations["object"]:
                        ds.isEnabled = False
                        ds.isEstop = True
                    break
                if time_left <= 0:
                    break

            if not self.field["isEstop"]:
                self.log("Match time expired, stopping match", "INFO")
                for ds in self.driverstations["object"]:
                    ds.isEnabled = False

                self.log("Match ended", "INFO")
        

    def close_sockets(self):
        for socket in self.driverstations["sockets"]:
            socket.close()
        self.log("Sockets closed", "INFO")