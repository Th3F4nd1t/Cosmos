# Cosmos FMS
An unofficial Field Management Software
<br>
Questions? Reach out to me on discord: @thefandit

## Features
- Multiple [modes](#modes)
- E-Stops and A-Stops
- Match timers and scoring for matches
- Logging and web access to logs
- Speed and port restrictions
- VLANs
- Security and internet access when needed
- Safety features including field "greenlighting" and optional automatic disconnection of robots
- Easy to use web interface for configuration and monitoring

### Modes
#### Development
- No restrictions on ports, speed, or anything else
- No VLANs
- No security
- No scoring
- No lights
- Only E-Stops work, A-Stops in auton-running
- Constant logging
- Internet access
#### Testing
- Restricted to official ports, speed, and other settings
- VLANs
- Security
- No scoring
- No lights
- Only E-Stops work, A-Stops in auton-running
- Constant logging
- No internet access
#### Match
- Restricted to official ports, speed, and other settings
- VLANs
- Security
- Scoring
- Lights
- E-Stops and A-Stops work
- Match timers and per match logs
- No internet access

## To Do
### Integrations
- Driverstation TCP send
- Driverstation TCP recieve
- Driverstation UDP send
- Driverstation UDP recieve
- Field AP write
- Field AP read
- PLC write
- PLC read
- Main switch write
- Red switch write
- Blue switch write
### Field states
- Null
- Off
- Booting
- Modeless
- Field-test
- Field-disabled
- Field-presentation
- Field-development
- Field-diagnostic
- Development-configuring
- Development-main
- Development-estop
- Development-greenlight
- Testing-configuring
- Testing-main
- Testing-estop
- Testing-greenlight
- Match-configuring
- Match-pre
- Match-autonomous
- Match-transition
- Match-teleop
- Match-endgame
- Match-abort
- Match-post
- Match-greenlight
- Crashed
- Shutting-down

## Priorities
- Estops
- Enable/disable robots
- Matches
- Logging
- Auto-scoring

## Development Notes
(Can ignore these, no longer applicable)
- Needs to be fully implemented, but all functions should be tagged with either `@user_run` or `@system_run` to indicate whether they should be run by the user or automatically by the system. For all user_run functions, all inputs/outputs should be via the to be implemented remote terminal ID system. For system_run functions, there should be no inputs, and all outputs should be broadcasted to all remote terminals, tagged with a priority level. If said remote terminal is at that level, it will display the broadcast. These system_run function's outputs will also always be logged. User run function's outputs can be logged, but that depends on the function.
- All functions should be tagged with `@mode` to indicate which mode they are available in.