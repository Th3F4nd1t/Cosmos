from enum import Enum
from network.tags import Tags, WPILibVersion
import datetime
from tools.terminal.decorators import user_run, system_run


class Station(Enum):
    RED_1 = 0x00
    RED_2 = 0x01
    RED_3 = 0x02
    BLUE_1 = 0x03
    BLUE_2 = 0x04
    BLUE_3 = 0x05

class DriverStationMode(Enum):
    TELEOP = 0x00
    TEST = 0x01
    AUTONOMOUS = 0x02

class DriverStationMatchType(Enum):
    TEST = 0x00
    PRACTICE = 0x01
    QUAL = 0x02
    PLAYOFF = 0x03


class UDPDriverStationPacket:
    def __init__(self):

        # Create basic fields to be filled before sending
        self.team_number:int = None
        self.station:Station = None
        
        self.packet_number:int = None

        self.isEstop:bool = None
        self.isAstop:bool = None
        self.isEnabled:bool = None

        self.mode:DriverStationMode = None

        self.match_type:DriverStationMatchType = None
        self.match_number:int = None
        self.repeat_number:int = None
        self.time_left:int = None

    def get(self):
        packet = bytearray(22)

        packet[0] = (self.packet_number >> 8) & 0xFF
        packet[1] = self.packet_number & 0xFF

        # Comm version
        packet[2] = 0x00

        # Control/status byte
        packet[3] = 0x00
        if self.isEstop: packet[3] |= 0b10000000
        if self.isAstop: packet[3] |= 0b01000000
        if self.isEnabled: packet[3] |= 0b00000100
        packet[3] |= self.mode.value

        # /shrug
        packet[4] = 0x00

        # station
        packet[5] = self.station.value

        # level
        packet[6] = self.match_type.value

        # match number
        packet[7] = bytes(self.match_number)[1] if self.match_number > 0xFF else 0x00
        packet[8] = bytes(self.match_number)[0]

        # repeat number
        packet[9] = bytes(self.repeat_number)[0]

        # date
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

        return packet
    
class TCPDriverStationPacket:
    ...

class UDPFMSPacket:
    def __init__(self):
        
        # Create basic fields to be filled before sending
        self.team_number:int = None
        self.station:Station = None
        
        self.packet_number:int = None

        self.isEstop:bool = None
        self.isAstop:bool = None
        self.isEnabled:bool = None

        self.mode:DriverStationMode = None

        self.match_type:DriverStationMatchType = None
        self.match_number:int = None
        self.repeat_number:int = None
        self.time_left:int = None

    def get (self):
        packet = bytearray(22)

        packet[0] = (self.packet_number >> 8) & 0xFF
        packet[1] = self.packet_number & 0xFF

        # Comm version
            # I dont know what to do with this

        # Control/status byte
        packet[3] = 0X00
        if self

        



class TCPFMSPacket:
    ...
