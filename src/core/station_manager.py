from enum import Enum
import schedule
import time

from utils.ip import driverstation_ip
# from main import FMS
from network.ds_net import Station, DriverStationMode, DriverStationMatchType, UDPDriverStationPacket

class StationManager:
    def __init__(self, fms):
        """
        Initialize the StationManager with a station ID and team number.
        """
        self.fms = fms

        self.send_updates = True

        self.packet_numbers = [0] * 6  # One for each station

        schedule.every(0.5).seconds.do(self._send_udp_update)

    def run(self):
        # Sending updates and receiving packets should be handled here
        while True:
            schedule.run_pending()
            time.sleep(0.001)
        
    def _send_udp_update(self):
        """
        Send an update to the driver station via UDP.
        """
        # self.fms.network_handler.send_udp
        if self.send_updates:
            # red 1
            if self.fms.state_store.state["teams"][0]["ds_connected"]:
                r1_packet = UDPDriverStationPacket()

                r1_packet.team_number = self.fms.state_store.state["teams"][0].key
                r1_packet.station = Station.RED_1
                r1_packet.ip = driverstation_ip(r1_packet.team_number)

                r1_packet.packet_number = self.packet_numbers[0]

                r1_packet.isEstop = self.fms.state_store.state["teams"][0]["status"]["estop"]
                r1_packet.isAstop = self.fms.state_store.state["teams"][0]["status"]["astop"]
                r1_packet.isEnabled = self.fms.state_store.state["teams"][0]["status"]["enabled"]

                if self.fms.state_store.state["teams"][0]["status"]["state"] == "teleop":
                    r1_packet.mode = DriverStationMode.TELEOP
                elif self.fms.state_store.state["teams"][0]["status"]["state"] == "test":
                    r1_packet.mode = DriverStationMode.TEST
                elif self.fms.state_store.state["teams"][0]["status"]["state"] == "autonomous":
                    r1_packet.mode = DriverStationMode.AUTONOMOUS
                else:
                    r1_packet.mode = DriverStationMode.TELEOP

                if self.fms.state_store.state["match"]["type"] == "test":
                    r1_packet.match_type = DriverStationMatchType.TEST
                elif self.fms.state_store.state["match"]["type"] == "practice":
                    r1_packet.match_type = DriverStationMatchType.PRACTICE
                elif self.fms.state_store.state["match"]["type"] == "qualification":
                    r1_packet.match_type = DriverStationMatchType.QUAL
                elif self.fms.state_store.state["match"]["type"] == "playoff":
                    r1_packet.match_type = DriverStationMatchType.PLAYOFF
                else:
                    r1_packet.match_type = DriverStationMatchType.TEST

                r1_packet.match_number = self.fms.state_store.state["match"]["number"]
                r1_packet.repeat_number = self.fms.state_store.state["match"]["repeat"]
                r1_packet.time_left = self.fms.state_store.state["match"]["time_left"]

            # red 2
            if self.fms.state_store.state["teams"][1]["ds_connected"]:
                r2_packet = UDPDriverStationPacket()

                r2_packet.team_number = self.fms.state_store.state["teams"][1].key
                r2_packet.station = Station.RED_2
                r2_packet.ip = driverstation_ip(r2_packet.team_number)

                r2_packet.packet_number = self.packet_numbers[1]

                r2_packet.isEstop = self.fms.state_store.state["teams"][1]["status"]["estop"]
                r2_packet.isAstop = self.fms.state_store.state["teams"][1]["status"]["astop"]
                r2_packet.isEnabled = self.fms.state_store.state["teams"][1]["status"]["enabled"]

                if self.fms.state_store.state["teams"][1]["status"]["state"] == "teleop":
                    r2_packet.mode = DriverStationMode.TELEOP
                elif self.fms.state_store.state["teams"][1]["status"]["state"] == "test":
                    r2_packet.mode = DriverStationMode.TEST
                elif self.fms.state_store.state["teams"][1]["status"]["state"] == "autonomous":
                    r2_packet.mode = DriverStationMode.AUTONOMOUS
                else:
                    r2_packet.mode = DriverStationMode.TELEOP

                if self.fms.state_store.state["match"]["type"] == "test":
                    r2_packet.match_type = DriverStationMatchType.TEST
                elif self.fms.state_store.state["match"]["type"] == "practice":
                    r2_packet.match_type = DriverStationMatchType.PRACTICE
                elif self.fms.state_store.state["match"]["type"] == "qualification":
                    r2_packet.match_type = DriverStationMatchType.QUAL
                elif self.fms.state_store.state["match"]["type"] == "playoff":
                    r2_packet.match_type = DriverStationMatchType.PLAYOFF
                else:
                    r2_packet.match_type = DriverStationMatchType.TEST

                r2_packet.match_number = self.fms.state_store.state["match"]["number"]
                r2_packet.repeat_number = self.fms.state_store.state["match"]["repeat"]
                r2_packet.time_left = self.fms.state_store.state["match"]["time_left"]

            # red 3
            if self.fms.state_store.state["teams"][2]["ds_connected"]:
                r3_packet = UDPDriverStationPacket()

                r3_packet.team_number = self.fms.state_store.state["teams"][2].key
                r3_packet.station = Station.RED_3
                r3_packet.ip = driverstation_ip(r3_packet.team_number)

                r3_packet.packet_number = self.packet_numbers[2]

                r3_packet.isEstop = self.fms.state_store.state["teams"][2]["status"]["estop"]
                r3_packet.isAstop = self.fms.state_store.state["teams"][2]["status"]["astop"]
                r3_packet.isEnabled = self.fms.state_store.state["teams"][2]["status"]["enabled"]

                if self.fms.state_store.state["teams"][2]["status"]["state"] == "teleop":
                    r3_packet.mode = DriverStationMode.TELEOP
                elif self.fms.state_store.state["teams"][2]["status"]["state"] == "test":
                    r3_packet.mode = DriverStationMode.TEST
                elif self.fms.state_store.state["teams"][2]["status"]["state"] == "autonomous":
                    r3_packet.mode = DriverStationMode.AUTONOMOUS
                else:
                    r3_packet.mode = DriverStationMode.TELEOP

                if self.fms.state_store.state["match"]["type"] == "test":
                    r3_packet.match_type = DriverStationMatchType.TEST
                elif self.fms.state_store.state["match"]["type"] == "practice":
                    r3_packet.match_type = DriverStationMatchType.PRACTICE
                elif self.fms.state_store.state["match"]["type"] == "qualification":
                    r3_packet.match_type = DriverStationMatchType.QUAL
                elif self.fms.state_store.state["match"]["type"] == "playoff":
                    r3_packet.match_type = DriverStationMatchType.PLAYOFF
                else:
                    r3_packet.match_type = DriverStationMatchType.TEST

                r3_packet.match_number = self.fms.state_store.state["match"]["number"]
                r3_packet.repeat_number = self.fms.state_store.state["match"]["repeat"]
                r3_packet.time_left = self.fms.state_store.state["match"]["time_left"]

            # blue 1
            if self.fms.state_store.state["teams"][3]["ds_connected"]:
                b1_packet = UDPDriverStationPacket()

                b1_packet.team_number = self.fms.state_store.state["teams"][3].key
                b1_packet.station = Station.BLUE_1
                b1_packet.ip = driverstation_ip(b1_packet.team_number)

                b1_packet.packet_number = self.packet_numbers[3]

                b1_packet.isEstop = self.fms.state_store.state["teams"][3]["status"]["estop"]
                b1_packet.isAstop = self.fms.state_store.state["teams"][3]["status"]["astop"]
                b1_packet.isEnabled = self.fms.state_store.state["teams"][3]["status"]["enabled"]

                if self.fms.state_store.state["teams"][3]["status"]["state"] == "teleop":
                    b1_packet.mode = DriverStationMode.TELEOP
                elif self.fms.state_store.state["teams"][3]["status"]["state"] == "test":
                    b1_packet.mode = DriverStationMode.TEST
                elif self.fms.state_store.state["teams"][3]["status"]["state"] == "autonomous":
                    b1_packet.mode = DriverStationMode.AUTONOMOUS
                else:
                    b1_packet.mode = DriverStationMode.TELEOP

                if self.fms.state_store.state["match"]["type"] == "test":
                    b1_packet.match_type = DriverStationMatchType.TEST
                elif self.fms.state_store.state["match"]["type"] == "practice":
                    b1_packet.match_type = DriverStationMatchType.PRACTICE
                elif self.fms.state_store.state["match"]["type"] == "qualification":
                    b1_packet.match_type = DriverStationMatchType.QUAL
                elif self.fms.state_store.state["match"]["type"] == "playoff":
                    b1_packet.match_type = DriverStationMatchType.PLAYOFF
                else:
                    b1_packet.match_type = DriverStationMatchType.TEST

                b1_packet.match_number = self.fms.state_store.state["match"]["number"]
                b1_packet.repeat_number = self.fms.state_store.state["match"]["repeat"]
                b1_packet.time_left = self.fms.state_store.state["match"]["time_left"]

            # blue 2
            if self.fms.state_store.state["teams"][4]["ds_connected"]:
                b2_packet = UDPDriverStationPacket()

                b2_packet.team_number = self.fms.state_store.state["teams"][4].key
                b2_packet.station = Station.BLUE_2
                b2_packet.ip = driverstation_ip(b2_packet.team_number)

                b2_packet.packet_number = self.packet_numbers[4]

                b2_packet.isEstop = self.fms.state_store.state["teams"][4]["status"]["estop"]
                b2_packet.isAstop = self.fms.state_store.state["teams"][4]["status"]["astop"]
                b2_packet.isEnabled = self.fms.state_store.state["teams"][4]["status"]["enabled"]

                if self.fms.state_store.state["teams"][4]["status"]["state"] == "teleop":
                    b2_packet.mode = DriverStationMode.TELEOP
                elif self.fms.state_store.state["teams"][4]["status"]["state"] == "test":
                    b2_packet.mode = DriverStationMode.TEST
                elif self.fms.state_store.state["teams"][4]["status"]["state"] == "autonomous":
                    b2_packet.mode = DriverStationMode.AUTONOMOUS
                else:
                    b2_packet.mode = DriverStationMode.TELEOP

                if self.fms.state_store.state["match"]["type"] == "test":
                    b2_packet.match_type = DriverStationMatchType.TEST
                elif self.fms.state_store.state["match"]["type"] == "practice":
                    b2_packet.match_type = DriverStationMatchType.PRACTICE
                elif self.fms.state_store.state["match"]["type"] == "qualification":
                    b2_packet.match_type = DriverStationMatchType.QUAL
                elif self.fms.state_store.state["match"]["type"] == "playoff":
                    b2_packet.match_type = DriverStationMatchType.PLAYOFF
                else:
                    b2_packet.match_type = DriverStationMatchType.TEST

                b2_packet.match_number = self.fms.state_store.state["match"]["number"]
                b2_packet.repeat_number = self.fms.state_store.state["match"]["repeat"]
                b2_packet.time_left = self.fms.state_store.state["match"]["time_left"]

            # blue 3
            if self.fms.state_store.state["teams"][5]["ds_connected"]:
                b3_packet = UDPDriverStationPacket()

                b3_packet.team_number = self.fms.state_store.state["teams"][5].key
                b3_packet.station = Station.BLUE_3
                b3_packet.ip = driverstation_ip(b3_packet.team_number)

                b3_packet.packet_number = self.packet_numbers[5]

                b3_packet.isEstop = self.fms.state_store.state["teams"][5]["status"]["estop"]
                b3_packet.isAstop = self.fms.state_store.state["teams"][5]["status"]["astop"]
                b3_packet.isEnabled = self.fms.state_store.state["teams"][5]["status"]["enabled"]

                if self.fms.state_store.state["teams"][5]["status"]["state"] == "teleop":
                    b3_packet.mode = DriverStationMode.TELEOP
                elif self.fms.state_store.state["teams"][5]["status"]["state"] == "test":
                    b3_packet.mode = DriverStationMode.TEST
                elif self.fms.state_store.state["teams"][5]["status"]["state"] == "autonomous":
                    b3_packet.mode = DriverStationMode.AUTONOMOUS
                else:
                    b3_packet.mode = DriverStationMode.TELEOP

                if self.fms.state_store.state["match"]["type"] == "test":
                    b3_packet.match_type = DriverStationMatchType.TEST
                elif self.fms.state_store.state["match"]["type"] == "practice":
                    b3_packet.match_type = DriverStationMatchType.PRACTICE
                elif self.fms.state_store.state["match"]["type"] == "qualification":
                    b3_packet.match_type = DriverStationMatchType.QUAL
                elif self.fms.state_store.state["match"]["type"] == "playoff":
                    b3_packet.match_type = DriverStationMatchType.PLAYOFF
                else:
                    b3_packet.match_type = DriverStationMatchType.TEST

                b3_packet.match_number = self.fms.state_store.state["match"]["number"]
                b3_packet.repeat_number = self.fms.state_store.state["match"]["repeat"]
                b3_packet.time_left = self.fms.state_store.state["match"]["time_left"]

            # Increment packet numbers
            self.packet_numbers[0] += 1
            self.packet_numbers[1] += 1
            self.packet_numbers[2] += 1
            self.packet_numbers[3] += 1
            self.packet_numbers[4] += 1
            self.packet_numbers[5] += 1

            # send the packets
            if self.fms.state_store.state["teams"][0]["ds_connected"]:
                self.fms.network_handler.send_udp(r1_packet.ip, 1121, r1_packet.get())

            if self.fms.state_store.state["teams"][1]["ds_connected"]:
                self.fms.network_handler.send_udp(r2_packet.ip, 1121, r2_packet.get())

            if self.fms.state_store.state["teams"][2]["ds_connected"]:
                self.fms.network_handler.send_udp(r3_packet.ip, 1121, r3_packet.get())

            if self.fms.state_store.state["teams"][3]["ds_connected"]:
                self.fms.network_handler.send_udp(b1_packet.ip, 1121, b1_packet.get())

            if self.fms.state_store.state["teams"][4]["ds_connected"]:
                self.fms.network_handler.send_udp(b2_packet.ip, 1121, b2_packet.get())

            if self.fms.state_store.state["teams"][5]["ds_connected"]:
                self.fms.network_handler.send_udp(b3_packet.ip, 1121, b3_packet.get())