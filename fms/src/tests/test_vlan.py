import pytest
import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from network.vlan_utils import Vlan


class TestVlanEnum:
    """Test cases for the Vlan enum"""
    
    def test_red_vlans(self):
        """Test that RED station VLANs have correct values"""
        assert Vlan.RED1.value == 10
        assert Vlan.RED2.value == 20
        assert Vlan.RED3.value == 30
    
    def test_blue_vlans(self):
        """Test that BLUE station VLANs have correct values"""
        assert Vlan.BLUE1.value == 40
        assert Vlan.BLUE2.value == 50
        assert Vlan.BLUE3.value == 60
    
    def test_fms_vlan(self):
        """Test that FMS VLAN has correct value"""
        assert Vlan.FMS.value == 100
    
    def test_venue_vlan(self):
        """Test that VENUE VLAN has correct value"""
        assert Vlan.VENUE.value == 200
    
    def test_vlan_uniqueness(self):
        """Test that all VLAN values are unique"""
        vlan_values = [v.value for v in Vlan]
        assert len(vlan_values) == len(set(vlan_values)), "VLAN values should be unique"
    
    def test_vlan_count(self):
        """Test that we have the expected number of VLANs"""
        assert len(Vlan) == 8, "Should have 8 VLANs defined"
    
    def test_vlan_enum_members(self):
        """Test that all expected VLAN members exist"""
        expected_members = ['RED1', 'RED2', 'RED3', 'BLUE1', 'BLUE2', 'BLUE3', 'FMS', 'VENUE']
        actual_members = [v.name for v in Vlan]
        assert sorted(actual_members) == sorted(expected_members)
