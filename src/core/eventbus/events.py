from enum import Enum
from typing import Callable, Any, Dict



class _EventEnum(Enum):
    def __new__(cls, event_name: str, validator: Callable[[Any], bool]):
        obj = object.__new__(cls)
        obj._value_ = event_name
        obj._validator = validator
        return obj

    @property
    def name_str(self) -> str:
        return self.value  # same as _event_name

    def validate(self, payload: Any) -> bool:
        return self._validator(payload)



class GeneralEvent(_EventEnum):
    ERROR = ("error", lambda payload: isinstance(payload, dict) and isinstance(payload.get("error"), str))
    INFO = ("info", lambda payload: isinstance(payload, dict) and isinstance(payload.get("message"), str))
    WARNING = ("warning", lambda payload: isinstance(payload, dict) and isinstance(payload.get("message"), str))
    DEBUG = ("debug", lambda payload: isinstance(payload, dict) and isinstance(payload.get("message"), str))



class EventBusEvent(_EventEnum):
    SUBSCRIBED = ("eventbus_subscribed", lambda payload: isinstance(payload, dict) and isinstance(payload.get("event_type"), str) and isinstance(payload.get("callback"), str))
    UNSUBSCRIBED = ("eventbus_unsubscribed", lambda payload: isinstance(payload, dict) and isinstance(payload.get("event_type"), str) and isinstance(payload.get("callback"), str))
    WARNING = ("eventbus_warning", lambda payload: isinstance(payload, dict) and isinstance(payload.get("warning"), str))
    ERROR = ("eventbus_error", lambda payload: isinstance(payload, dict) and isinstance(payload.get("error"), str))



class MatchEvent(_EventEnum):
    PRESTARTED = ("match_prestarted", lambda payload: isinstance(payload, dict) and isinstance(payload.get("match_number"), int) and isinstance(payload.get("teams"), list) and all(isinstance(team, (int, None)) for team in payload.get("teams", [])))
    STARTED = ("match_started", lambda payload: isinstance(payload, dict) and isinstance(payload.get("match_number"), int) and isinstance(payload.get("teams"), list) and all(isinstance(team, (int, None)) for team in payload.get("teams", [])))
    PROGRESS = ("match_progress", lambda payload: isinstance(payload, dict) and isinstance(payload.get("match_number"), int) and isinstance(payload.get("progression"), str))
    ENDED = ("match_ended", lambda payload: isinstance(payload, dict) and isinstance(payload.get("match_number"), int) and isinstance(payload.get("teams"), list) and all(isinstance(team, (int, None)) for team in payload.get("teams", [])))
    ERROR = ("match_error", lambda payload: isinstance(payload, dict) and isinstance(payload.get("error"), str))



class RobotEvent(_EventEnum):
    FIELD_ESTOP = ("field_estop", lambda payload: isinstance(payload, dict) and isinstance(payload.get("active"), bool) and isinstance(payload.get("reason"), str))
    ESTOP = ("robot_estop", lambda payload: isinstance(payload, dict) and isinstance(payload.get("active"), bool) and isinstance(payload.get("team_number"), int) and isinstance(payload.get("reason"), str))
    ASTOP = ("robot_astop", lambda payload: isinstance(payload, dict) and isinstance(payload.get("active"), bool) and isinstance(payload.get("team_number"), int) and isinstance(payload.get("reason"), str))
    CONTROLLER_CONNECTED = ("robot_controller_connected", lambda payload: isinstance(payload, dict) and isinstance(payload.get("team_number"), int))
    CONTROLLER_DISCONNECTED = ("robot_controller_disconnected", lambda payload: isinstance(payload, dict) and isinstance(payload.get("team_number"), int))
    CONTROLLER_ERROR = ("robot_controller_error", lambda payload: isinstance(payload, dict) and isinstance(payload.get("team_number"), int) and isinstance(payload.get("error"), str))
    RADIO_CONNECTED = ("robot_radio_connected", lambda payload: isinstance(payload, dict) and isinstance(payload.get("team_number"), int))
    RADIO_DISCONNECTED = ("robot_radio_disconnected", lambda payload: isinstance(payload, dict) and isinstance(payload.get("team_number"), int))
    RADIO_ERROR = ("robot_radio_error", lambda payload: isinstance(payload, dict) and isinstance(payload.get("team_number"), int) and isinstance(payload.get("error"), str))
    DS_CONNECTED = ("robot_ds_connected", lambda payload: isinstance(payload, dict) and isinstance(payload.get("team_number"), int))
    DS_DISCONNECTED = ("robot_ds_disconnected", lambda payload: isinstance(payload, dict) and isinstance(payload.get("team_number"), int))
    DS_ERROR = ("robot_ds_error", lambda payload: isinstance(payload, dict) and isinstance(payload.get("team_number"), int) and isinstance(payload.get("error"), str))



class PLCEvent(_EventEnum):
    REMOTE_SERVER_STARTED = ("plc_remote_server_started", lambda payload: isinstance(payload, dict) and isinstance(payload.get("station"), str) and isinstance(payload.get("ip"), str))
    REMOTE_SERVER_STOPPED = ("plc_remote_server_stopped", lambda payload: isinstance(payload, dict) and isinstance(payload.get("station"), str) and isinstance(payload.get("ip"), str))
    REMOTE_SERVER_ERROR = ("plc_remote_server_error", lambda payload: isinstance(payload, dict) and isinstance(payload.get("station"), str) and isinstance(payload.get("ip"), str) and isinstance(payload.get("error"), str))
    LIGHT_SET = ("plc_light_set", lambda payload: isinstance(payload, dict) and isinstance(payload.get("station"), str) and isinstance(payload.get("color"), str))
    LIGHT_ERROR = ("plc_light_error", lambda payload: isinstance(payload, dict) and isinstance(payload.get("station"), str) and isinstance(payload.get("error"), str))
    NUMBER_SET = ("plc_number_set", lambda payload: isinstance(payload, dict) and isinstance(payload.get("station"), str) and isinstance(payload.get("number"), int))
    NUMBER_ERROR = ("plc_number_error", lambda payload: isinstance(payload, dict) and isinstance(payload.get("station"), str) and isinstance(payload.get("error"), str))
    


class StateEvent(_EventEnum):
    CHANGED = ("state_changed", lambda payload: isinstance(payload, dict) and isinstance(payload.get("state"), str) and isinstance(payload.get("previous_state"), str) and isinstance(payload.get("reason"), str))
    ERROR = ("state_error", lambda payload: isinstance(payload, dict) and isinstance(payload.get("error"), str))
    REQUEST = ("state_request", lambda payload: isinstance(payload, dict) and isinstance(payload.get("state"), str) and isinstance(payload.get("requestor"), str) and isinstance(payload.get("force"), bool))



class SwitchEvent(_EventEnum):
    CONFIGURED = ("switch_configured", lambda payload: isinstance(payload, dict) and isinstance(payload.get("switch"), str) and isinstance(payload.get("config_desc"), str))
    ERROR = ("switch_error", lambda payload: isinstance(payload, dict) and isinstance(payload.get("switch"), str) and isinstance(payload.get("error"), str))



class TeamEvent(_EventEnum):
    ADDED = ("team_added", lambda payload: isinstance(payload, dict) and isinstance(payload.get("team_number"), int) and isinstance(payload.get("team_name"), str))
    REMOVED = ("team_removed", lambda payload: isinstance(payload, dict) and isinstance(payload.get("team_number"), int))
    UPDATED = ("team_updated", lambda payload: isinstance(payload, dict) and isinstance(payload.get("team_number"), int) and isinstance(payload.get("team_name"), str))
    ERROR = ("team_error", lambda payload: isinstance(payload, dict) and isinstance(payload.get("error"), str) and isinstance(payload.get("team_number"), int))



class UserAttentionEvent(_EventEnum):
    ADDED = ("user_attention_item_added", lambda payload: isinstance(payload, dict) and isinstance(payload.get("item"), str) and isinstance(payload.get("idn"), int) and isinstance(payload.get("forced"), bool))
    REMOVED = ("user_attention_item_removed", lambda payload: isinstance(payload, dict) and isinstance(payload.get("item"), str) and isinstance(payload.get("idn"), int))
    RESOLVED = ("user_attention_item_resolved", lambda payload: isinstance(payload, dict) and isinstance(payload.get("item"), str) and isinstance(payload.get("idn"), int))
    ERROR = ("user_attention_item_error", lambda payload: isinstance(payload, dict) and isinstance(payload.get("item"), str) and isinstance(payload.get("idn"), int) and isinstance(payload.get("error"), str))



class TerminalEvent(_EventEnum):
    CONNECTED = ("terminal_connected", lambda payload: isinstance(payload, dict) and isinstance(payload.get("id"), int) and isinstance(payload.get("type"), str))
    DISCONNECTED = ("terminal_disconnected", lambda payload: isinstance(payload, dict) and isinstance(payload.get("id"), int))
    COMMAND = ("terminal_command", lambda payload: isinstance(payload, dict) and isinstance(payload.get("id"), int) and isinstance(payload.get("command"), str))
    RESPONSE = ("terminal_response", lambda payload: isinstance(payload, dict) and isinstance(payload.get("id"), int) and isinstance(payload.get("response"), str) and isinstance(payload.get("level"), str))
    BROADCAST = ("terminal_broadcast", lambda payload: isinstance(payload, dict) and isinstance(payload.get("message"), str) and isinstance(payload.get("level"), str))
    ERROR = ("terminal_error", lambda payload: isinstance(payload, dict) and isinstance(payload.get("id"), int) and isinstance(payload.get("error"), str))