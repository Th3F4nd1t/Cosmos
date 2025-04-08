import datetime
from enum import Enum
from scapy.all import Ether, Dot1Q, IP, UDP, sendp

from ds import DriverStation, AllianceStation

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
                DriverStation(3767, AllianceStation.RED1),
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
            
        }

        self.field = {
            "mode" : ArenaMode.TEST,
            "match_number" : 1,
            "time_left" : 0,
        }

    def log(self, message: str, level: str = "INFO"):
        levels = {
            "INFO": "\033[94m",
            "WARNING": "\033[93m",
            "ERROR": "\033[91m",
            "DEBUG": "\033[92m"
        }
        reset = "\033[0m"
        print(f"{levels.get(level, reset)}[{level}] {reset}{message}")

    def loop(self):
        # Get from PLCs
        # Get from API
        # Update field state
        # Send to DS
        # Send to PLCs        
        ...

    def send_udp(self, station: AllianceStation, tags: list = None):
        packet = bytearray(22)

        # Packet number, stored big-endian
        packet[0] = bytes([self.driverstations["object"][station].packet_number])[1] if self.driverstations["object"][station].packet_number > 0xFF else 0x00
        packet[1] = bytes([self.driverstations["object"][station].packet_number])[0]

        # Comm version
        packet[2] = 0x00

        # Control/status byte
        packet[3] = 0
        if self.driverstations["object"][station].isEstop: packet[3] |= 0b10000000
        if self.driverstations["object"][station].isAstop: packet[3] |= 0b01000000
        if self.driverstations["object"][station].isEnabled: packet[3] |= 0b00000100
        packet[3] |= self.driverstations["object"][station].mode

        # Unknown or unused
        packet[4] = 0x00

        # Alliance station
        packet[5] = station

        # Tournament level
        if self.field["mode"] == ArenaMode.TEST:
            packet[6] = 0x00
        elif self.field["mode"] == ArenaMode.PRACTICE_MATCH:
            packet[6] = 0x01
        elif self.field["mode"] == ArenaMode.QUAL_MATCH:
            packet[6] = 0x02
        elif self.field["mode"] == ArenaMode.PLAYOFF_MATCH:
            packet[6] = 0x03
        elif self.field["mode"] == ArenaMode.DEVELOPMENT:
            packet[6] = 0x02
        elif self.field["mode"] == ArenaMode.NO_FMS:
            packet[6] = 0x02
        else:
            packet[6] = 0x00
            self.log("Unknown arena mode", "ERROR")
            
        # Match number
        packet[7] = bytes([self.field["match_number"]])[1] if self.field["match_number"] > 0xFF else 0x00
        packet[8] = bytes([self.field["match_number"]])[0]
        packet[9] = 0x01 # Repeat number

        # Date
        now = datetime.datetime.now(datetime.timezone.utc)

        packet[10] = int(now.microsecond).to_bytes(4, byteorder="big")[0]
        packet[11] = int(now.microsecond).to_bytes(4, byteorder="big")[1]
        packet[12] = int(now.microsecond).to_bytes(4, byteorder="big")[2]
        packet[13] = int(now.microsecond).to_bytes(4, byteorder="big")[3]
        packet[14] = now.second.to_bytes(1, byteorder="big")[0]
        packet[15] = now.minute.to_bytes(1, byteorder="big")[0]
        packet[16] = now.hour.to_bytes(1, byteorder="big")[0]
        packet[17] = now.day.to_bytes(1, byteorder="big")[0]
        packet[18] = (now.month - 1).to_bytes(1, byteorder="big")[0]
        packet[19] = (now.year - 1900).to_bytes(1, byteorder="big")[0]

        # Remaining time
        packet[20] = bytes([self.field["time_left"]])[1] if self.field["time_left"] > 0xFF else 0x00
        packet[21] = bytes([self.field["time_left"]])[0]

        # Increment packet number
        self.driverstations["object"][station].packet_number += 1

        if self.driverstations["object"][station].packet_number > 0xFFFF:
            self.driverstations["object"][station].packet_number = 0x0000
            self.log("Packet number overflow", "WARNING")

        # Send packet to DS
        self.log(f"Sending packet to {station} ({self.driverstations['object'][station].ip})", "DEBUG")
        for byte in packet:
            self.log(f"{byte:08b}", "DEBUG")
        self.log(f"Packet length: {len(packet)}", "DEBUG")
        

if __name__ == "__main__":
    arena = Arena()
    arena.log("Arena started", "INFO")
    arena.log("Sending packet to RED1", "INFO")
    while True:
        arena.send_udp(AllianceStation.RED1)