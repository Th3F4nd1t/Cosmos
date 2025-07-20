from enum import Enum
import schedule
import time

from utils.ip import driverstation_ip
# from main import FMS
from network.ds_net import Station, DriverStationMode, DriverStationMatchType, UDPDriverStationPacket
from core.eventbus.events import GeneralEvent

class StationManager:
    def __init__(self, fms):
        """
        Initialize the StationManager with a station ID and team number.
        """
        self.fms = fms

        self.send_updates = True

        self.packet_numbers = [0] * 6  # One for each station

        schedule.every(0.5).seconds.do(self._send_udp_update)
        # schedule.every(1).seconds.do(self.test_emitter)

    def run(self):
        # Sending updates and receiving packets should be handled here
        while True:
            schedule.run_pending()
            time.sleep(0.001)

    # def test_emitter(self):
    #     self.fms.emit(GeneralEvent.INFO, {"message": "Test message from StationManager"})

    def _send_udp_update(self):
        """
        Send an update to the driver station via UDP.
        """
        # self.fms.network_handler.send_udp
        for i in range(0, 6):
            if self.send_updates:
                # red 1
                if self.fms.state_store.state["teams"][i].ds_connected:
                    packet = UDPDriverStationPacket()

                    packet.team_number = self.fms.state_store.state["teams"][i].key
                    packet.station = i
                    packet.ip = driverstation_ip(packet.team_number)

                    packet.packet_number = self.packet_numbers[i]

                    packet.isEstop = self.fms.state_store.state["teams"][i]["status"]["estop"]
                    packet.isAstop = self.fms.state_store.state["teams"][i]["status"]["astop"]
                    packet.isEnabled = self.fms.state_store.state["teams"][i]["status"]["enabled"]

                    if self.fms.state_store.state["teams"][i]["status"]["state"] == "teleop":
                        packet.mode = DriverStationMode.TELEOP
                    elif self.fms.state_store.state["teams"][i]["status"]["state"] == "test":
                        packet.mode = DriverStationMode.TEST
                    elif self.fms.state_store.state["teams"][i]["status"]["state"] == "autonomous":
                        packet.mode = DriverStationMode.AUTONOMOUS
                    else:
                        packet.mode = DriverStationMode.TELEOP

                    if self.fms.state_store.state["match"]["type"] == "test":
                        packet.match_type = DriverStationMatchType.TEST
                    elif self.fms.state_store.state["match"]["type"] == "practice":
                        packet.match_type = DriverStationMatchType.PRACTICE
                    elif self.fms.state_store.state["match"]["type"] == "qualification":
                        packet.match_type = DriverStationMatchType.QUAL
                    elif self.fms.state_store.state["match"]["type"] == "playoff":
                        packet.match_type = DriverStationMatchType.PLAYOFF
                    else:
                        packet.match_type = DriverStationMatchType.TEST

                    packet.match_number = self.fms.state_store.state["match"]["number"]
                    packet.repeat_number = self.fms.state_store.state["match"]["repeat"]
                    packet.time_left = self.fms.state_store.state["match"]["time_left"]

                    self.fms.network_handler.send_udp(packet.ip, 1121, packet.get())

                self.packet_numbers[i] += 1