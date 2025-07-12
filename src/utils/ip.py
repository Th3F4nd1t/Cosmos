from enum import Enum
from tools.terminal.decorators import user_run, system_run

@system_run
def driverstation_ip(team: int) -> str:
    """
    Returns the Driver Station IP for a given FRC team number.
    Format depends on number of digits in the team number.
    """
    try:
        team = int(team)
    except ValueError:
        raise ValueError("Team number must be an integer for DS IP")

    if not (0 < team <= 25599):
        raise ValueError("Invalid team number for DS IP")
    

    team_str = str(team).zfill(5)  # pad to 5 digits to simplify slicing


    if team < 100:  # 1 or 2 digits
        return ip(10, 0, team, 5)
    elif team < 1000:  # 3 digits
        return ip(10, int(team_str[0]), int(team_str[1:]), 5)
    elif team < 10000:  # 4 digits
        return ip(10, int(team_str[:2]), int(team_str[2:]), 5)
    else:  # 5 digits
        return ip(10, int(team_str[:3]), int(team_str[3:]), 5)
    

class ip:
    @system_run
    def __init__(self, a:int, b:int, c:int, d:int):
        """
        Initializes an IP address.
        """
        if not (0 <= a <= 255 and 0 <= b <= 255 and 0 <= c <= 255 and 0 <= d <= 255):
            raise ValueError(f"Invalid IP address: {a}.{b}.{c}.{d}")
        self.ip = f"{a}.{b}.{c}.{d}"

    @system_run
    def get(self) -> str:
        return self.ip
    

class IP(Enum):
    RED_PLC = "10.0.100.200"
    BLUE_PLC = "10.0.100.201"
    MAIN_PLC = "10.0.100.202"

    RED_SWITCH = "10.0.100.100"
    BLUE_SWITCH = "10.0.100.101"
    MAIN_SWITCH = "10.0.100.102"

    