Events will be published to the event bus with a string event type and a dictionary data payload.
Valid event types and associated data payloads are found in the below tables seperated by class of event.

#### General Events
| Event Type      | Data Payload                                      |
|------------------|---------------------------------------------------|
| `robot_estop`       | `{ "team_number": <team_number:int>, "reason": <reason:str> }` |
| `robot_astop`      | `{ "team_number": <robot_team_numberid:int>, "reason": <reason:str> }` |

#### Match Events
| Event Type      | Data Payload                                      |
|------------------|---------------------------------------------------|
| `match_started`     | `{ "number": <match_number:int>, "teams": <team_list:list[int]> }` |
| `match_error`       | `{ "error": <error_message:str> }`                       |

