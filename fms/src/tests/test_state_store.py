import pytest
import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.state_store import StateStore, States, RobotState, MatchType, TeamData, State
from network.ds_net import Station


class TestState:
    """Test cases for the State class"""
    
    def test_state_creation(self):
        """Test creating a State object"""
        state = State("test", "Test State", "A test state", ["next1", "next2"])
        assert state.name == "test"
        assert state.human_name == "Test State"
        assert state.description == "A test state"
        assert state.next_states == ["next1", "next2"]
    
    def test_state_get_name(self):
        """Test get_name method"""
        state = State("test", "Test State", "A test state", [])
        assert state.get_name() == "test"
    
    def test_state_get_human_name(self):
        """Test get_human_name method"""
        state = State("test", "Test State", "A test state", [])
        assert state.get_human_name() == "Test State"
    
    def test_state_get_description(self):
        """Test get_description method"""
        state = State("test", "Test State", "A test state", [])
        assert state.get_description() == "A test state"
    
    def test_state_get_next_states(self):
        """Test get_next_states method"""
        state = State("test", "Test State", "A test state", ["next1", "next2"])
        assert state.get_next_states() == ["next1", "next2"]


class TestStatesEnum:
    """Test cases for the States enum"""
    
    def test_states_enum_has_off(self):
        """Test that OFF state exists"""
        assert hasattr(States, 'OFF')
        assert States.OFF.value.name == "off"
    
    def test_states_enum_has_match_states(self):
        """Test that match-related states exist"""
        assert hasattr(States, 'MATCH_PRE')
        assert hasattr(States, 'MATCH_AUTONOMOUS')
        assert hasattr(States, 'MATCH_TELEOP')
        assert hasattr(States, 'MATCH_ENDGAME')
        assert hasattr(States, 'MATCH_POST')
    
    def test_states_enum_has_development_states(self):
        """Test that development-related states exist"""
        assert hasattr(States, 'DEVELOPMENT_CONFIGURING')
        assert hasattr(States, 'DEVELOPMENT_MAIN')
        assert hasattr(States, 'DEVELOPMENT_ESTOP')
        assert hasattr(States, 'DEVELOPMENT_GREENLIGHT')
    
    def test_states_enum_has_testing_states(self):
        """Test that testing-related states exist"""
        assert hasattr(States, 'TESTING_CONFIGURING')
        assert hasattr(States, 'TESTING_MAIN')
        assert hasattr(States, 'TESTING_ESTOP')
        assert hasattr(States, 'TESTING_GREENLIGHT')


class TestRobotStateEnum:
    """Test cases for the RobotState enum"""
    
    def test_robot_state_values(self):
        """Test that RobotState enum has correct values"""
        assert RobotState.DISABLED.value == 0
        assert RobotState.AUTO.value == 1
        assert RobotState.TELEOP.value == 2
        assert RobotState.TEST.value == 3


class TestMatchTypeEnum:
    """Test cases for the MatchType enum"""
    
    def test_match_type_values(self):
        """Test that MatchType enum has correct values"""
        assert MatchType.TEST.value == "test"
        assert MatchType.PRACTICE.value == "practice"
        assert MatchType.QUALIFICATION.value == "qualification"
        assert MatchType.PLAYOFF.value == "playoff"


class TestTeamData:
    """Test cases for the TeamData class"""
    
    def test_team_data_creation(self):
        """Test creating a TeamData object"""
        team = TeamData(
            number=1234,
            name="Test Team",
            ip="10.12.34.5",
            ds_connected=True,
            radio_connected=True,
            rio_connected=True,
            state=RobotState.TELEOP,
            estop=False,
            astop=False,
            enabled=True
        )
        assert team.number == 1234
        assert team.name == "Test Team"
        assert team.ip == "10.12.34.5"
        assert team.ds_connected is True
        assert team.radio_connected is True
        assert team.rio_connected is True
        assert team.state == RobotState.TELEOP
        assert team.estop is False
        assert team.astop is False
        assert team.enabled is True
    
    def test_team_data_get(self):
        """Test TeamData.get() method returns proper dict"""
        team = TeamData(
            number=1234,
            name="Test Team",
            ip="10.12.34.5",
            ds_connected=True,
            radio_connected=False,
            rio_connected=True,
            state=RobotState.AUTO,
            estop=False,
            astop=False,
            enabled=True
        )
        result = team.get()
        assert result is not None
        assert result["number"] == 1234
        assert result["name"] == "Test Team"
        assert result["ip"] == "10.12.34.5"
        assert result["status"]["ds_connected"] is True
        assert result["status"]["radio_connected"] is False
        assert result["status"]["rio_connected"] is True
        assert result["status"]["state"] == RobotState.AUTO
        assert result["status"]["estop"] is False
        assert result["status"]["astop"] is False
        assert result["status"]["enabled"] is True
    
    def test_team_data_get_incomplete_returns_none(self):
        """Test that TeamData.get() returns None if data is incomplete"""
        team = TeamData(number=1234)  # Missing required fields
        result = team.get()
        assert result is None


class TestStateStore:
    """Test cases for the StateStore class"""
    
    def test_state_store_initialization(self):
        """Test that StateStore initializes with default values"""
        store = StateStore()
        assert store.is_running() is True
        assert store.get_state() == States.NULL
        assert len(store.get_teams()) == 6
    
    def test_set_and_get_running(self):
        """Test setting and getting running state"""
        store = StateStore()
        store.set_running(False)
        assert store.is_running() is False
        store.set_running(True)
        assert store.is_running() is True
    
    def test_set_running_invalid_type(self):
        """Test that setting running with non-bool raises TypeError"""
        store = StateStore()
        with pytest.raises(TypeError):
            store.set_running("True")
        with pytest.raises(TypeError):
            store.set_running(1)
    
    def test_set_and_get_state(self):
        """Test setting and getting FMS state"""
        store = StateStore()
        store.set_state(States.MATCH_PRE)
        assert store.get_state() == States.MATCH_PRE
        store.set_state(States.DEVELOPMENT_MAIN)
        assert store.get_state() == States.DEVELOPMENT_MAIN
    
    def test_set_state_invalid_type(self):
        """Test that setting state with non-States raises TypeError"""
        store = StateStore()
        with pytest.raises(TypeError):
            store.set_state("match-pre")
    
    def test_set_and_get_team_number(self):
        """Test setting and getting team number"""
        store = StateStore()
        store.set_team_number(Station.RED_1, 1234)
        assert store.get_team_number(Station.RED_1) == 1234
    
    def test_set_team_number_invalid_station(self):
        """Test that setting team number with invalid station raises TypeError"""
        store = StateStore()
        with pytest.raises(TypeError):
            store.set_team_number(0, 1234)
    
    def test_set_team_number_invalid_number(self):
        """Test that setting team number with invalid number raises TypeError"""
        store = StateStore()
        with pytest.raises(TypeError):
            store.set_team_number(Station.RED_1, "1234")
    
    def test_set_and_get_team_name(self):
        """Test setting and getting team name"""
        store = StateStore()
        store.set_team_name(Station.BLUE_2, "Awesome Team")
        assert store.get_team_name(Station.BLUE_2) == "Awesome Team"
    
    def test_set_and_get_team_ip(self):
        """Test setting and getting team IP"""
        store = StateStore()
        store.set_team_ip(Station.RED_2, "10.12.34.5")
        assert store.get_team_ip(Station.RED_2) == "10.12.34.5"
    
    def test_set_and_get_team_ds_connected(self):
        """Test setting and getting team DS connected status"""
        store = StateStore()
        store.set_team_ds_connected(Station.BLUE_1, True)
        assert store.get_team_ds_connected(Station.BLUE_1) is True
        store.set_team_ds_connected(Station.BLUE_1, False)
        assert store.get_team_ds_connected(Station.BLUE_1) is False
    
    def test_set_and_get_team_radio_connected(self):
        """Test setting and getting team radio connected status"""
        store = StateStore()
        store.set_team_radio_connected(Station.RED_3, True)
        assert store.get_team_radio_connected(Station.RED_3) is True
    
    def test_set_and_get_team_rio_connected(self):
        """Test setting and getting team RIO connected status"""
        store = StateStore()
        store.set_team_rio_connected(Station.BLUE_3, True)
        assert store.get_team_rio_connected(Station.BLUE_3) is True
    
    def test_set_and_get_team_state(self):
        """Test setting and getting team robot state"""
        store = StateStore()
        store.set_team_state(Station.RED_1, RobotState.AUTO)
        assert store.get_team_state(Station.RED_1) == RobotState.AUTO
        store.set_team_state(Station.RED_1, RobotState.TELEOP)
        assert store.get_team_state(Station.RED_1) == RobotState.TELEOP
    
    def test_set_and_get_team_estop(self):
        """Test setting and getting team E-Stop status"""
        store = StateStore()
        store.set_team_estop(Station.BLUE_2, True)
        assert store.get_team_estop(Station.BLUE_2) is True
        store.set_team_estop(Station.BLUE_2, False)
        assert store.get_team_estop(Station.BLUE_2) is False
    
    def test_set_and_get_team_astop(self):
        """Test setting and getting team A-Stop status"""
        store = StateStore()
        store.set_team_astop(Station.RED_2, True)
        assert store.get_team_astop(Station.RED_2) is True
    
    def test_set_and_get_team_enabled(self):
        """Test setting and getting team enabled status"""
        store = StateStore()
        store.set_team_enabled(Station.BLUE_1, True)
        assert store.get_team_enabled(Station.BLUE_1) is True
        store.set_team_enabled(Station.BLUE_1, False)
        assert store.get_team_enabled(Station.BLUE_1) is False
    
    def test_get_teams(self):
        """Test getting all teams"""
        store = StateStore()
        teams = store.get_teams()
        assert len(teams) == 6
        assert all(isinstance(team, TeamData) for team in teams)
    
    def test_set_and_get_match_number(self):
        """Test setting and getting match number"""
        store = StateStore()
        store.set_match_number(42)
        assert store.get_match_number() == 42
    
    def test_set_match_number_invalid_type(self):
        """Test that setting match number with invalid type raises TypeError"""
        store = StateStore()
        with pytest.raises(TypeError):
            store.set_match_number("42")
    
    def test_set_and_get_match_repeat(self):
        """Test setting and getting match repeat"""
        store = StateStore()
        store.set_match_repeat(2)
        assert store.get_match_repeat() == 2
    
    def test_set_and_get_match_type(self):
        """Test setting and getting match type"""
        store = StateStore()
        store.set_match_type(MatchType.QUALIFICATION)
        assert store.get_match_type() == MatchType.QUALIFICATION
        store.set_match_type(MatchType.PLAYOFF)
        assert store.get_match_type() == MatchType.PLAYOFF
    
    def test_set_and_get_match_time_left(self):
        """Test setting and getting match time left"""
        store = StateStore()
        store.set_match_time_left(135)
        assert store.get_match_time_left() == 135
    
    def test_set_and_get_match_progression(self):
        """Test setting and getting match progression"""
        store = StateStore()
        progression = [
            [States.MATCH_AUTONOMOUS, 15],
            [States.MATCH_TELEOP, 135]
        ]
        store.set_match_progression(progression)
        assert store.get_match_progression() == progression
    
    def test_set_match_progression_invalid_type(self):
        """Test that setting match progression with invalid type raises TypeError"""
        store = StateStore()
        with pytest.raises(TypeError):
            store.set_match_progression("not a list")
    
    def test_set_match_progression_invalid_structure(self):
        """Test that setting match progression with invalid structure raises TypeError"""
        store = StateStore()
        with pytest.raises(TypeError):
            store.set_match_progression([[States.MATCH_AUTONOMOUS]])  # Missing time
    
    def test_get_state_dict(self):
        """Test getting the complete state dictionary"""
        store = StateStore()
        state_dict = store.get()
        assert isinstance(state_dict, dict)
        assert "running" in state_dict
        assert "state" in state_dict
        assert "teams" in state_dict
        assert "match" in state_dict
