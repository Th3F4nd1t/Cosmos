# Enums for driverstations
from enum import Enum

class ContolMode(Enum):
    TELEOP = 0b00000000
    TEST = 0b00000001
    AUTONOMOUS = 0b00000010

def ControlByte(isEstop: bool, isAstop: bool, isEnabled: bool, mode: ContolMode):
    control_byte = 0b00000000

    if isEstop: control_byte |= 0b10000000
    if isAstop: control_byte |= 0b01000000
    if isEnabled: control_byte |= 0b00000100
    control_byte |= mode

    return control_byte

class AllianceStation(Enum):
    RED1 = 0b00000000
    RED2 = 0b00000001
    RED3 = 0b00000010
    BLUE1 = 0b00000011
    BLUE2 = 0b00000100
    BLUE3 = 0b00000101

class TournamentLevel(Enum):
    MATCHTEST = 0b00000000
    PRACTICE = 0b00000001
    QUALIFICATION = 0b00000010
    PLAYOFF = 0b00000011

class Tags(Enum):
    ...

