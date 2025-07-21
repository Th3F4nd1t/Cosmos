from enum import Enum
import logging
from netmiko import ConnectHandler
from src.core.eventbus.events import GeneralEvent, SwitchEvent


class SwitchConfigMetadata:
    def __init__(self, description: str=None, version: str=None, author: str=None):
        self.description = description
        self.version = version
        self.author = author

class SwitchConfig:
    def __init__(self, config: dict, metadata: SwitchConfigMetadata):
        self.config = config
        self.metadata: SwitchConfigMetadata = metadata


class SwitchType(Enum):
    CISCO_IOS = "CISCO_IOS"
    CISCO_NXOS = "CISCO_NXOS"
    CISCO_S300 = "CISCO_S300"
    CISCO_SMB = "CISCO_SMB"
    MAIN = ...
    STATION = ...


class SwitchHandler:
    def __init__(self, name: str, ip: str, username: str, password: str, switch_type: SwitchType, fms=None):
        if fms is None:
            raise ValueError("FMS instance must be provided")
        else:
            self.fms = fms

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
        self.fms.emit(GeneralEvent.INFO, {"message": f"Config added to switch {self.name}"})

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
                self.fms.emit(SwitchEvent.CONFIGURED, {"switch": f"{self.name}", "config_desc": self.metadata.description if self.metadata else "No description"})
                conn.save_config()
                conn.disconnect()

            except Exception as e:
                self.fms.emit(SwitchEvent.ERROR, {"switch": f"{self.name}", "error": f"Failed to configure switch {self.name}: {str(e)}"})

            conn.send_config_set(self.config)

            self.fms.emit(GeneralEvent.INFO, {"message": f"Config pushed to switch {self.name}"})
        else:
            self.fms.emit(GeneralEvent.WARNING, {"message": f"No config to push to switch {self.name}"})