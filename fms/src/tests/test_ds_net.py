import pytest
import sys
from pathlib import Path
import datetime

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from network.ds_net import Station, DriverStationMode, DriverStationMatchType, UDPDriverStationPacket


class TestStationEnum:
    """Test cases for the Station enum"""
    
    def test_station_values(self):
        """Test that Station enum has correct values"""
        assert Station.RED_1.value == 0x00
        assert Station.RED_2.value == 0x01
        assert Station.RED_3.value == 0x02
        assert Station.BLUE_1.value == 0x03
        assert Station.BLUE_2.value == 0x04
        assert Station.BLUE_3.value == 0x05
    
    def test_station_count(self):
        """Test that we have exactly 6 stations"""
        assert len(Station) == 6
    
    def test_station_uniqueness(self):
        """Test that all station values are unique"""
        values = [s.value for s in Station]
        assert len(values) == len(set(values))


class TestDriverStationModeEnum:
    """Test cases for the DriverStationMode enum"""
    
    def test_mode_values(self):
        """Test that DriverStationMode enum has correct values"""
        assert DriverStationMode.TELEOP.value == 0x00
        assert DriverStationMode.TEST.value == 0x01
        assert DriverStationMode.AUTONOMOUS.value == 0x02
    
    def test_mode_count(self):
        """Test that we have exactly 3 modes"""
        assert len(DriverStationMode) == 3


class TestDriverStationMatchTypeEnum:
    """Test cases for the DriverStationMatchType enum"""
    
    def test_match_type_values(self):
        """Test that DriverStationMatchType enum has correct values"""
        assert DriverStationMatchType.TEST.value == 0x00
        assert DriverStationMatchType.PRACTICE.value == 0x01
        assert DriverStationMatchType.QUAL.value == 0x02
        assert DriverStationMatchType.PLAYOFF.value == 0x03
    
    def test_match_type_count(self):
        """Test that we have exactly 4 match types"""
        assert len(DriverStationMatchType) == 4


class TestUDPDriverStationPacket:
    """Test cases for the UDPDriverStationPacket class"""
    
    def test_packet_initialization(self):
        """Test that packet initializes with None values"""
        packet = UDPDriverStationPacket()
        assert packet.team_number is None
        assert packet.station is None
        assert packet.packet_number is None
        assert packet.isEstop is None
        assert packet.isAstop is None
        assert packet.isEnabled is None
        assert packet.mode is None
        assert packet.match_type is None
        assert packet.match_number is None
        assert packet.repeat_number is None
        assert packet.time_left is None
    
    def test_packet_field_assignment(self):
        """Test that packet fields can be assigned"""
        packet = UDPDriverStationPacket()
        packet.team_number = 1234
        packet.station = Station.RED_1
        packet.packet_number = 1
        packet.isEstop = False
        packet.isAstop = True
        packet.isEnabled = True
        packet.mode = DriverStationMode.TELEOP
        packet.match_type = DriverStationMatchType.QUAL
        packet.match_number = 42
        packet.repeat_number = 0
        packet.time_left = 135
        
        # Verify assignments
        assert packet.team_number == 1234
        assert packet.station == Station.RED_1
        assert packet.packet_number == 1
        assert packet.isEstop is False
        assert packet.isAstop is True
        assert packet.isEnabled is True
        assert packet.mode == DriverStationMode.TELEOP
        assert packet.match_type == DriverStationMatchType.QUAL
        assert packet.match_number == 42
        assert packet.repeat_number == 0
        assert packet.time_left == 135

