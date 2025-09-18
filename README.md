# Cosmos FMS
An unofficial Field Management Software
<br>
I have files for specific deployments, but they are not included here **AND ARE REQUIRED FOR PROPER OPERATION**. Please contact me if you want them. Also can contact me for help setting up/finding parts/or really anything.
<br>
discord: @thefandit
<br>
(For FIRST YPP, you must be under 18 to DM me, otherwise ping me in the FRC discord server: https://discord.gg/frc)

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


## Roles
- Default (D)
    - Has E-Stop access
- Team Member (TM)
    - Can be approved for a specific team by a FH/FM (for a period of time), or permanently by an FA
    - Can see most information having to do with their team/robot
    - Has E-Stop access
- Field Helper (FH)
    - Can be approved by an FM (for a period of time), or permanently by an FA
    - Can see most information having to do with the field
    - Can't change states or settings
    - Has E-Stop access
- Field Manager (FM)
    - Can be approved by an FA
    - Can start matches
    - Can go into most required states
    - Has E-Stop access
- Field Admin (FA)
    - Can be approved by an FA
    - Needed for any development/diagnostics
    - Can go into all states
    - Can change all settings
    - Has E-Stop and A-Stop access


## Webserver stack
- Flask
- nginx
- cloudflared


## Server files
- /opt/cosmos/
    - fms/
        - src/
            - fms.py
        - logs/
        - webserver/
            - src/
                - webserver.py
            - logs/

- /etc/systemd/system/
    - cosmos.service
    - cloudflared.service
    - webserver.service

- /etc/nginx/sites-available/
    - cosmos.conf

- /etc/cloudflared/
    - config.yml


## Ports
- 8080 (webserver traffic)
- 8090 (webserver/fms socket)
