import datetime
from enum import Enum
import socket

class Station:
    RED1 = 0x00
    RED2 = 0x01
    RED3 = 0x02
    BLUE1 = 0x03
    BLUE2 = 0x04
    BLUE3 = 0x05

class DriverStationMode(Enum):
    TELEOP = 0x00
    TEST = 0x01
    AUTONOMOUS = 0x02

class DriverStationMatchType(Enum):
    TEST = 0x00
    PRACTICE = 0x01
    QUAL = 0x02
    PLAYOFF = 0x03

class DriverStation:
    def __init__(self, team_number: int|None, station_number: Station, ip: str = None, vlan: int = None):
        self.team_number = team_number if team_number != None else 0
        self.station_number = station_number

        self.ip =  ip if ip != None else f"10.{self.team_number // 100}.{self.team_number % 100}.5"
        self.vlan = vlan if vlan != None else (station_number + 1) * 10

        self.packet_number = 0

        self.isEstop = False
        self.isAstop = False
        self.isEnabled = False

        self.mode = DriverStationMode.TELEOP

        self.match_type = DriverStationMatchType.TEST
        self.match_number = 0
        self.repeat_number = 1
        self.time_left = 0

        self.udp_send_port = 1120
        self.udp_send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.tcp_send_port = 1750
        self.tcp_send_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_send_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.udp_recv_port = 1160
        self.udp_recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.tcp_recv_port = 1750
        self.tcp_recv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send_udp(self, tags: list = None):
        packet = bytearray(22)

        packet[0] = (self.packet_number >> 8) & 0xFF  # High byte
        packet[1] = self.packet_number & 0xFF         # Low byte

        # Comm version
        packet[2] = 0x00

        # Control/status byte
        packet[3] = 0
        if self.isEstop: packet[3] |= 0b10000000
        if self.isAstop: packet[3] |= 0b01000000
        if self.isEnabled: packet[3] |= 0b00000100
        packet[3] |= self.mode

        # Unknown or unused
        packet[4] = 0x00

        # Alliance station
        packet[5] = self.station_number

        # Tournament level
        packet[6] = self.match_type
            
        # Match number
        packet[7] = bytes(self.match_number)[1] if self.match_number > 0xFF else 0x00
        packet[8] = bytes(self.match_number)[0]
        packet[9] = bytes(self.repeat_number)[0]

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
        packet[20] = bytes(int(self.time_left))[1] if self.time_left > 0xFF else 0x00
        packet[21] = bytes(int(self.time_left))[0]

        # Increment packet number
        self.packet_number += 1

        if self.packet_number > 0xFFFF:
            self.packet_number = 0x0000
            self.log("Packet number overflow", "WARNING")

        self.sock.sendto(packet, (self.ip, self.udp_send_port))

    def enable(self):
        self.isEnabled = True
        print("enabled:" + str(self.station_number))

    def disable(self):
        self.isEnabled = False
        print("disabled:" + str(self.station_number))