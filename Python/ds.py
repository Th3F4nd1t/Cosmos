

class ToDsUDP:
    """
    Sent to the DS every 500ms on UDP port 1121 (force FMS connection) or 1120 (ask to approve connection).
    sequence_num - 2B - uint16
    comm_version - 1B - uint8
    control_byte - 1B - ControlByte
    request_byte - 1B - 0x00
    allience_station - 1B - AllianceStation
    tournament_level - 1B - TournamentLevel
    match_num - 2B - uint16
    play_num - 1B - uint8
    date - 10B - Date
    remaining_time - 2B - uint16
    tags - nB - Tags (Offseason FMS has code, but no tags are used)
    """

class ToDsTCP:
    """
    UDP stands for 
    """

class FromDsUDP:
    ...

class FromDsTCP:
    ...



class AllianceStation:
    RED1 = 0
    RED2 = 1
    RED3 = 2
    BLUE1 = 3
    BLUE2 = 4
    BLUE3 = 5

class DriverStation:
    def __init__(self, team_number: int|None, station_number: AllianceStation, ip: str = None, vlan: int = None):
        self.team_number = team_number if team_number != None else 0
        self.station_number = station_number
        self.ip =  ip if ip != None else f"10.{self.team_number // 100}.{self.team_number % 100}.5"
        self.vlan = vlan if vlan != None else (station_number + 1) * 10

    def set_team_num(self, team_number: int):
        self.team_number = team_number
        self.ip = f"10.{self.team_number // 100}.{self.team_number % 100}.5"