import requests
import time

class DriverStation:
    def __init__(self, vlan):
        self.team_number = None
        self.robot_ip = None
        self.ip = None

        self.vlan = vlan
        self.is_connected = False
        self.is_estopped = False
        self.is_ds_attached = False
        self.is_robot_linked = False

    def set_team_number(self, team_number):
        self.team_number = team_number
        self.robot_ip = f"10.{team_number // 100}.{team_number % 100}.2"
        self.ip = f"10.{team_number // 100}.{team_number % 100}.5"

    def get_status(self):
        return {
            "isConnected": self.is_connected,
            "isEstopped": self.is_estopped,
            "isDSAttached": self.is_ds_attached,
            "isRobotLinked": self.is_robot_linked,
            "isRobotRunning": False
        }

    def enable_robot(self):
        if not self.is_estopped:
            pass

    def disable_robot(self):
        pass

    def check_connection(self):
        pass

    def estop(self):
        self.disable_robot()
        self.is_estopped = True
