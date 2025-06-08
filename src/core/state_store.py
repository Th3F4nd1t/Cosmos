
from enum import Enum
from typing import Any, List


class State:
    name: str
    human_name: str
    description: str
    next_states: List[str]

    def __init__(self, name: str, human_name: str, description: str, next_states: List[str]):
        self.name:str = name
        self.human_name:str = human_name
        self.description:str = description
        self.next_states:List[str] = next_states

    def get_name(self) -> str:
        """
        Get the name of the state.
        """
        return self.name
    
    def get_human_name(self) -> str:
        """
        Get the human-readable name of the state.
        """
        return self.human_name
    
    def get_description(self) -> str:
        """
        Get the description of the state.
        """
        return self.description
    
    def get_next_states(self) -> List[str]:
        """
        Get the next possible states.
        """
        return self.next_states
    


class States(Enum):
    """
    Enum class to handle various FMS states.
    """

    NULL = State(
        "null",
        "null",
        "The FMS is in an invalid state.",
        ["*"]
    )
    OFF = State(
        "off",
        "off",
        "The FMS is in the off state.",
        ["booting", "crashed"]
    )
    BOOTING = State(
        "booting",
        "booting",
        "The FMS is in the booting state.",
        ["modeless", "crashed"]
    )
    MODELESS = State(
        "modeless",
        "modeless",
        "The FMS is in the modeless state.",
        ["field-test", "field-disabled", "field-presentation", "field-development", "field-diagnostic", "development-configuring", "testing-configuring", "match-configuring", "shutting-down", "crashed"]
    )
    FIELD_TEST = State(
        "field-test",
        "field-test",
        "The FMS is in the field-test state.",
        ["modeless", "testing-main", "crashed"]
    )
    FIELD_DISABLED = State(
        "field-disabled",
        "field-disabled",
        "The FMS is in the field-disabled state.",
        ["modeless", "crashed"]
    )
    FIELD_PRESENTATION = State(
        "field-presentation",
        "field-presentation",
        "The FMS is in the field-presentation state.",
        ["modeless", "crashed"]
    )
    FIELD_DEVELOPMENT = State(
        "field-development",
        "field-development",
        "The FMS is in the field-development state.",
        ["modeless", "crashed"]
    )
    FIELD_DIAGNOSTIC = State(
        "field-diagnostic",
        "field-diagnostic",
        "The FMS is in the field-diagnostic state.",
        ["modeless", "crashed"]
    )
    DEVELOPMENT_CONFIGURING = State(
        "development-configuring",
        "development-configuring",
        "The FMS is in the development-configuring state.",
        ["development-main", "crashed"]
    )
    DEVELOPMENT_MAIN = State(
        "development-main",
        "development-main",
        "The FMS is in the development-main state.",
        ["development-estop", "development-greenlight", "crashed"]
    )
    DEVELOPMENT_ESTOP = State(
        "development-estop",
        "development-estop",
        "The FMS is in the development-estop state.",
        ["modeless", "development-greenlight", "crashed"]
    )
    DEVELOPMENT_GREENLIGHT = State(
        "development-greenlight",
        "development-greenlight",
        "The FMS is in the development-greenlight state.",
        ["modeless", "development-configuring", "crashed"]
    )
    TESTING_CONFIGURING = State(
        "testing-configuring",
        "testing-configuring",
        "The FMS is in the testing-configuring state.",
        ["testing-estop", "testing-greenlight", "crashed"]
    )
    TESTING_MAIN = State(
        "testing-main",
        "testing-main",
        "The FMS is in the testing-main state.",
        ["testing-configuring", "testing-estop", "testing-greenlight", "crashed"]
    )
    TESTING_ESTOP = State(
        "testing-estop",
        "testing-estop",
        "The FMS is in the testing-estop state.",
        ["modeless", "testing-configuring", "testing-greenlight", "crashed"]
    )
    TESTING_GREENLIGHT = State(
        "testing-greenlight",
        "testing-greenlight",
        "The FMS is in the testing-greenlight state.",
        ["modeless", "testing-configuring", "crashed"]
    )
    MATCH_CONFIGURING = State(
        "match-configuring",
        "match-configuring",
        "The FMS is in the match-configuring state.",
        ["match-pre", "crashed"]
    )
    MATCH_PRE = State(
        "match-pre",
        "match-pre",
        "The FMS is in the match-pre state.",
        ["match-configuring", "match-autonomous", "match-abort", "match-greenlight", "crashed"]
    )
    MATCH_AUTONOMOUS = State(
        "match-autonomous",
        "match-autonomous",
        "The FMS is in the match-autonomous state.",
        ["match-transition", "match-abort", "crashed"]
    )
    MATCH_TRANSITION = State(
        "match-transition",
        "match-transition",
        "The FMS is in the match-transition state.",
        ["match-teleop", "match-abort", "crashed"]
    )
    MATCH_TELEOP = State(
        "match-teleop",
        "match-teleop",
        "The FMS is in the match-teleop state.",
        ["match-endgame", "match-abort", "match-post", "crashed"]
    )
    MATCH_ENDGAME = State(
        "match-endgame",
        "match-endgame",
        "The FMS is in the match-endgame state.",
        ["match-abort", "match-post", "crashed"]
    )
    MATCH_ABORT_OR_ESTOP = State(
        "match-abort",
        "match-abort",
        "The FMS is in the match-abort state.",
        ["modeless", "match-configuring", "match-post", "match-greenlight", "crashed"]
    )
    MATCH_POST = State(
        "match-post",
        "match-post",
        "The FMS is in the match-post state.",
        ["modeless", "match-configuring", "match-greenlight", "crashed"]
    )
    MATCH_GREENLIGHT = State(
        "match-greenlight",
        "match-greenlight",
        "The FMS is in the match-greenlight state.",
        ["modeless", "match-configuring", "match-post", "crashed"]
    )
    CRASHED = State(
        "crashed",
        "crashed",
        "The FMS is in the crashed state.",
        ["booting", "modeless"]
    )
    SHUTTING_DOWN = State(
        "shutting-down",
        "shutting-down",
        "The FMS is in the shutting-down state.",
        ["crashed", "off"]
    )


class StateStore:
    def __init__(self):
        self.state:dict[str, Any] = {
            "state" : States.NULL,
            "teams" : {
                "1" : {
                    "ip" : "10.0.1.5",
                    "status" : {
                        "ds_connected" : False,
                        "radio_connected" : False,
                        "rio_connected" : False,
                        "state" : "disabled", # disabled, auto, teleop, test
                        "estop" : False,
                        "astop" : False,
                        "enabled" : False # True if the robot is enabled, False otherwise
                    }
                },
                "2" : {
                    "ip" : "10.0.2.5",
                    "status" : {
                        "ds_connected" : False,
                        "radio_connected" : False,
                        "rio_connected" : False,
                        "state" : "disabled", # disabled, auto, teleop, test
                        "estop" : False,
                        "astop" : False,
                        "enabled" : False
                    }
                },
                "3" : {
                    "ip" : "10.0.3.5",
                    "status" : {
                        "ds_connected" : False,
                        "radio_connected" : False,
                        "rio_connected" : False,
                        "state" : "disabled", # disabled, auto, teleop, test
                        "estop" : False,
                        "astop" : False,
                        "enabled" : False
                    }
                },
                "4" : {
                    "ip" : "10.0.4.5",
                    "status" : {
                        "ds_connected" : False,
                        "radio_connected" : False,
                        "rio_connected" : False,
                        "state" : "disabled", # disabled, auto, teleop, test
                        "estop" : False,
                        "astop" : False,
                        "enabled" : False
                    }
                },
                "5" : {
                    "ip" : "10.0.5.5",
                    "status" : {
                        "ds_connected" : False,
                        "radio_connected" : False,
                        "rio_connected" : False,
                        "state" : "disabled", # disabled, auto, teleop, test
                        "estop" : False,
                        "astop" : False,
                        "enabled" : False
                    }
                },
                "6" : {
                    "ip" : "10.0.6.5",
                    "status" : {
                        "ds_connected" : False,
                        "radio_connected" : False,
                        "rio_connected" : False,
                        "state" : "disabled", # disabled, auto, teleop, test
                        "estop" : False,
                        "astop" : False,
                        "enabled" : False
                    }
                },
            },
            "match" : {
                "number" : 0,
                "repeat" : 0,
                "type" : "test", # test, practice, qualification, playoff
                "time_left" : -1,
                "progression" : [ # state, time
                    [States.MATCH_AUTONOMOUS, 15],
                    [States.MATCH_TRANSITION, 1],
                    [States.MATCH_TELEOP, 115],
                    [States.MATCH_ENDGAME, 20],
                    [States.MATCH_POST, 5]
                ]
            }
        }
        

    def set_state(self, state: States):
        """
        Set the current state of the FMS.
        """
        self.state["state"] = state

    def get_state(self) -> States:
        """
        Get the current state of the FMS.
        """
        return self.state["state"]
    