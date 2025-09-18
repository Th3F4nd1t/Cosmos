Events will be published to the event bus with a string event type and a dictionary data payload.
Valid event types and associated data payloads are found in the below tables seperated by class of event, which generally corrospond to the file or class from which they originate.
<br>
Event enums are found in [`core.eventbus.events`](https://github.com/Th3F4nd1t/Cosmos/tree/main/src/core/eventbus/events.py)

#### General Events
| Event Type      | Data Payload                                      |
|------------------|---------------------------------------------------|
| `error` | `{ "error": <error_message:str> }`                       |
| `info`  | `{ "message": <message:str> }`                       |
| `debug` | `{ "message": <message:str> }`                       |
| `warning` | `{ "message": <message:str> }`                       |

#### EventBus
| Event Type      | Data Payload                                      |
|------------------|---------------------------------------------------|
| `eventbus_subscribed` | `{ "event_type": <event_type:str>, "callback": <callback:str> }` |
| `eventbus_unsubscribed` | `{ "event_type": <event_type:str>, "callback": <callback:str> }` |
| `eventbus_warning` | `{ "warning": <warning_message:str> }` |
| `eventbus_error` | `{ "error": <error_message:str> }`                       |

#### Match Events
| Event Type      | Data Payload                                      |
|------------------|---------------------------------------------------|
| `match_prestarted`     | `{ "number": <match_number:int>, "teams": <team_list:list[int]> }` |
| `match_started`     | `{ "number": <match_number:int>, "teams": <team_list:list[int]> }` |
| `match_progression` | `{ "number": <match_number:int>, "progression": <progression:str> }` |
| `match_ended`       | `{ "number": <match_number:int>, "teams": <team_list:list[int]> }` |
| `match_error`       | `{ "error": <error_message:str> }`                       |

#### Robot Events
| Event Type      | Data Payload                                      |
|------------------|---------------------------------------------------|
| `field_estop`       | `{ "active": <active:bool>, "reason": <reason:str> }` |
| `robot_estop`       | `{ "active": <active:bool>, "team_number": <team_number:int>, "reason": <reason:str> }` |
| `robot_astop`      | `{ "active": <active:bool>, "team_number": <robot_team_numberid:int>, "reason": <reason:str> }` |
| `robot_controller_connected`   | `{ "team_number": <team_number:int> }` |
| `robot_controller_disconnected`| `{ "team_number": <team_number:int> }` |
| `robot_controller_error`       | `{ "team_number": <team_number:int>, "error": <error_message:str> }` |
| `robot_radio_connected`   | `{ "team_number": <team_number:int> }` |
| `robot_radio_disconnected`| `{ "team_number": <team_number:int> }` |
| `robot_radio_error`       | `{ "team_number": <team_number:int>, "error": <error_message:str> }` |
| `robot_ds_connected`   | `{ "team_number": <team_number:int> }` |
| `robot_ds_disconnected`| `{ "team_number": <team_number:int> }` |
| `robot_ds_error`       | `{ "team_number": <team_number:int>, "error": <error_message:str> }` |

#### PLC Events
| Event Type      | Data Payload                                      |
|------------------|---------------------------------------------------|
| `plc_remote_server_started` | `{ "station": <station:str>, "ip": <ip:str> }` |
| `plc_remote_server_stopped` | `{ "station": <station:str>, "ip": <ip:str> }` |
| `plc_remote_server_error`   | `{ "station": <station:str>, "ip": <ip:str>, "error": <error_message:str> }` |
| `plc_light_set` | `{ "station": <station:str>, "color": <color:str> }` |
| `plc_light_error`   | `{ "station": <station:str>, "error": <error_message:str> }` |
| `plc_number_set` | `{ "station": <station:str>, "number": <number:int> }` |
| `plc_number_error`   | `{ "station": <station:str>, "error": <error_message:str> }` |

#### State Events
| Event Type      | Data Payload                                      |
|------------------|---------------------------------------------------|
| `state_changed` | `{ "state": <state:str>, "previous_state": <previous_state:str>, "reason": <reason:str> }` |
| `state_error`   | `{ "error": <error_message:str> }` |
| `state_request` | `{ "state": <state:str>, "requestor": <requestor:str>, "force": <force:bool> }` |

#### Swtich Events
| Event Type      | Data Payload                                      |
|------------------|---------------------------------------------------|
| `switch_configured` | `{ "switch": <switch_name:str>, "config_desc": <config_desc:str> }` |
| `switch_error` | `{ "switch": <switch_name:str>, "error": <error_message:str> }` |

#### Team Events
| Event Type      | Data Payload                                      |
|------------------|---------------------------------------------------|
| `team_added` | `{ "team_number": <team_number:int>, "team_name": <team_name:str> }` |
| `team_removed` | `{ "team_number": <team_number:int> }` |
| `team_updated` | `{ "team_number": <team_number:int>, "team_name": <team_name:str> }` |
| `team_error` | `{ "team_number": <team_number:int>, "error": <error_message:str> }` |

#### User Attention Events
| Event Type      | Data Payload                                      |
|------------------|---------------------------------------------------|
| `user_attention_item_added` | `{ "item": <item:str>, "idn": <idn:int>, "forced": <forced:bool> }` |
| `user_attention_item_removed` | `{ "item": <item:str>, "idn": <idn:int> }` |
| `user_attention_item_resolved` | `{ "item": <item:str>, "idn": <idn:int> }` |
| `user_attention_item_error` | `{ "item": <item:str>, "idn": <idn:int>, "error": <error_message:str> }` |

#### Terminal Events
| Event Type      | Data Payload                                      |
|------------------|---------------------------------------------------|
| `terminal_connected` | `{ "id": <terminal_id:int>, "type": <terminal_type:str> }` |
| `terminal_disconnected` | `{ "id": <terminal_id:int> }` |
| `terminal_command` | `{ "id": <terminal_id:int>, "command": <command:str> }` |
| `terminal_response` | `{ "id": <terminal_id:int>, "response": <response:str>, "level": <level:str> }` |
| `terminal_broadcast` | `{ "message": <message:str>, "level": <level:str> }` |
| `terminal_error` | `{ "id": <terminal_id:int>, "error": <error_message:str> }` |
