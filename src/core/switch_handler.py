from enum import Enum
import logging
from netmiko import ConnectHandler

logger = logging.getLogger("switch_handler")

class SwitchConfig:
    def __init__(self, config: dict, metadata: dict):
        self.config = config
        self.metadata = metadata


class SwitchType(Enum):
    CISCO_IOS = "CISCO_IOS"
    CISCO_NXOS = "CISCO_NXOS"
    CISCO_S300 = "CISCO_S300"
    CISCO_SMB = "CISCO_SMB"
    MAIN = ...
    STATION = ...


class SwitchHandler:
    def __init__(self, name: str, ip: str, username: str, password: str, switch_type: SwitchType):
        self.name = name
        self.ip = ip
        self.username = username
        self.password = password
        self.config = None
        self.metadata = None
        self.switch_type = switch_type

    def add_config(self, config: SwitchConfig):
        self.config = config.config
        self.metadata = config.metadata
        logger.log(f"Config added.")

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
                logger.info(f"Config pushed to {self.name}.")
                logger.log(output)
                conn.save_config()
                conn.disconnect()

            except Exception as e:

                logger.error(f"Failed to configure {self.name}: {e}")

            conn.send_config_set(self.config)

            logger.log(f"Config pushed.")
        else:
            logger.log(f"No config to push.")