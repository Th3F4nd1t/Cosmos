from enum import Enum
from logger import Logger
from netmiko import ConnectHandler


class SwitchConfig:
    def __init__(self, config: dict, metadata: dict):
        self.config = config
        self.metadata = metadata


class SwitchType(Enum):
    CISCO_IOS = "CISCO_IOS"
    CISCO_NXOS = "CISCO_NXOS"
    CISCO_S300 = "CISCO_S300"
    CISCO_SMB = "CISCO_SMB"


class Switch:
    def __init__(self, name: str, ip: str, username: str, password: str, switch_type: SwitchType):
        self.name = name
        self.ip = ip
        self.username = username
        self.password = password
        self.config = None
        self.metadata = None
        self.logger = Logger(f"{name}-switch")

    def add_config(self, config: SwitchConfig):
        self.config = config.config
        self.metadata = config.metadata
        self.logger.log(f"Config added.")

    def push_config(self):
        if self.config:
            try:
                conn = ConnectHandler(
                    device_type=self.switch_type.value,
                    host=self.ip,
                    username=self.username,
                    password=self.password,
                )

                output = conn.send_config_set(self.config)
                self.logger.info(f"Config pushed to {self.name}.")
                self.logger.log(output)
                conn.save_config()
                conn.disconnect()

            except Exception as e:

                self.logger.error(f"Failed to configure {self.name}: {e}")

            conn.send_config_set(self.config)

            self.logger.log(f"Config pushed.")
        else:
            self.logger.log(f"No config to push.")


class SwitchHandler:
    def __init__(self):
        self.logger = Logger("SwitchHandler")
        self.switches = []
        self.logger.log("SwitchHandler initialized")
        for switch in self.switches:
            self.logger.log(f"Switch {switch.name} added with IP {switch.ip}")

    def add_switch(self, switch: Switch):
        self.switches.append(switch)
        self.logger.log(f"Switch {switch.name} added with IP {switch.ip}")

    def push_config(self):
        for switch in self.switches:
            if switch.config:
                switch.push_config()
                self.logger.log(f"Config pushed to {switch.name} with IP {switch.ip}")
            else:
                self.logger.log(f"No config found for {switch.name} with IP {switch.ip}")

    def add_config(self, switch_name: str, config: SwitchConfig):
        for switch in self.switches:
            if switch.name == switch_name:
                switch.add_config(config)
                self.logger.log(f"Config added to {switch.name} with IP {switch.ip}")
                return
        self.logger.log(f"Switch {switch_name} not found")