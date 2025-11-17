import pytest
import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.ip import ip, team_ip, driverstation_ip, IP


class TestIPClass:
    """Test cases for the ip class"""
    
    def test_valid_ip_creation(self):
        """Test creating a valid IP address"""
        test_ip = ip(192, 168, 1, 1)
        assert test_ip.get() == "192.168.1.1"
    
    def test_ip_with_zeros(self):
        """Test creating an IP address with zeros"""
        test_ip = ip(10, 0, 0, 1)
        assert test_ip.get() == "10.0.0.1"
    
    def test_ip_with_max_values(self):
        """Test creating an IP address with maximum valid values"""
        test_ip = ip(255, 255, 255, 255)
        assert test_ip.get() == "255.255.255.255"
    
    def test_invalid_ip_high_value(self):
        """Test that IP creation fails with values > 255"""
        with pytest.raises(ValueError, match="Invalid IP address"):
            ip(256, 0, 0, 1)
        
        with pytest.raises(ValueError, match="Invalid IP address"):
            ip(10, 256, 0, 1)
        
        with pytest.raises(ValueError, match="Invalid IP address"):
            ip(10, 0, 256, 1)
        
        with pytest.raises(ValueError, match="Invalid IP address"):
            ip(10, 0, 0, 256)
    
    def test_invalid_ip_negative_value(self):
        """Test that IP creation fails with negative values"""
        with pytest.raises(ValueError, match="Invalid IP address"):
            ip(-1, 0, 0, 1)
        
        with pytest.raises(ValueError, match="Invalid IP address"):
            ip(10, -1, 0, 1)
        
        with pytest.raises(ValueError, match="Invalid IP address"):
            ip(10, 0, -1, 1)
        
        with pytest.raises(ValueError, match="Invalid IP address"):
            ip(10, 0, 0, -1)


class TestTeamIP:
    """Test cases for the team_ip function"""
    
    def test_single_digit_team(self):
        """Test IP generation for single digit team numbers"""
        # Team 1 -> 10.0.1.x
        assert team_ip(1, 5) == "10.0.1.5"
        assert team_ip(9, 5) == "10.0.9.5"
    
    def test_two_digit_team(self):
        """Test IP generation for two digit team numbers"""
        # Team 25 -> 10.0.25.x
        assert team_ip(25, 5) == "10.0.25.5"
        assert team_ip(99, 5) == "10.0.99.5"
    
    def test_three_digit_team(self):
        """Test IP generation for three digit team numbers"""
        # Team 100 -> 10.0.100.x (100-999 use third octet)
        assert team_ip(100, 5) == "10.0.100.5"
        assert team_ip(123, 5) == "10.0.123.5"
        assert team_ip(255, 5) == "10.0.255.5"
    
    def test_four_digit_team(self):
        """Test IP generation for four digit team numbers"""
        # Team 1000 -> 10.1.0.x (splits first digit and last 3)
        assert team_ip(1000, 5) == "10.1.0.5"
        assert team_ip(1234, 5) == "10.1.234.5"
        assert team_ip(9255, 5) == "10.9.255.5"
    
    def test_five_digit_team(self):
        """Test IP generation for five digit team numbers"""
        # Team 12345 -> 10.123.45.x
        assert team_ip(10000, 5) == "10.100.0.5"
        assert team_ip(12345, 5) == "10.123.45.5"
        assert team_ip(25599, 5) == "10.255.99.5"
    
    def test_different_end_octets(self):
        """Test that different end octets work correctly"""
        assert team_ip(1234, 1) == "10.1.234.1"
        assert team_ip(1234, 100) == "10.1.234.100"
        assert team_ip(1234, 255) == "10.1.234.255"
    
    def test_invalid_team_number_zero(self):
        """Test that team number 0 is invalid"""
        with pytest.raises(ValueError, match="Invalid team number for DS IP"):
            team_ip(0, 5)
    
    def test_invalid_team_number_negative(self):
        """Test that negative team numbers are invalid"""
        with pytest.raises(ValueError, match="Invalid team number for DS IP"):
            team_ip(-1, 5)
    
    def test_invalid_team_number_too_high(self):
        """Test that team numbers above 25599 are invalid"""
        with pytest.raises(ValueError, match="Invalid team number for DS IP"):
            team_ip(25600, 5)
        
        with pytest.raises(ValueError, match="Invalid team number for DS IP"):
            team_ip(100000, 5)
    
    def test_invalid_team_number_non_integer(self):
        """Test that non-integer team numbers are invalid"""
        with pytest.raises(ValueError, match="Team number must be an integer for DS IP"):
            team_ip("abc", 5)


class TestDriverstationIP:
    """Test cases for the driverstation_ip function"""
    
    def test_driverstation_ip_single_digit(self):
        """Test driverstation IP for single digit team"""
        assert driverstation_ip(1) == "10.0.1.5"
    
    def test_driverstation_ip_two_digit(self):
        """Test driverstation IP for two digit team"""
        assert driverstation_ip(25) == "10.0.25.5"
    
    def test_driverstation_ip_three_digit(self):
        """Test driverstation IP for three digit team"""
        assert driverstation_ip(123) == "10.0.123.5"
    
    def test_driverstation_ip_four_digit(self):
        """Test driverstation IP for four digit team"""
        assert driverstation_ip(1234) == "10.1.234.5"
    
    def test_driverstation_ip_five_digit(self):
        """Test driverstation IP for five digit team"""
        assert driverstation_ip(12345) == "10.123.45.5"


class TestIPEnum:
    """Test cases for the IP enum"""
    
    def test_plc_ips(self):
        """Test that PLC IPs are correct"""
        assert IP.RED_PLC.value == "10.0.100.200"
        assert IP.BLUE_PLC.value == "10.0.100.201"
        assert IP.MAIN_PLC.value == "10.0.100.202"
    
    def test_switch_ips(self):
        """Test that Switch IPs are correct"""
        assert IP.RED_SWITCH.value == "10.0.100.100"
        assert IP.BLUE_SWITCH.value == "10.0.100.101"
        assert IP.MAIN_SWITCH.value == "10.0.100.102"
