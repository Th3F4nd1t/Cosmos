# Cosmos FMS
An unofficial Field Management Software
<br>
I have files for specific deployments, but they are not included here **AND ARE REQUIRED FOR PROPER OPERATION**. Please contact me if you want them. Also can contact me for help setting up/fi```jaanding parts/or really anything.
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
### Switch configs
- Disabled
- Unmanaged
- Development
- Testing
- Match
Syntax:
    <&station_1@team_number>
    <&station_1@team_name>
    <&station_1@ip>

    <&plc_red@ip>
    <&plc_blue@ip>

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
- 22 (SSH)
- 8070 (PLC communication)
- 8080 (webserver traffic)
- 8090 (webserver/fms socket)


# Network Infrastructure
## 1. Core Network Infrastructure
### 1.1 Core Switch
Purpose: Acts as the layer 3 gateway for all VLANs, routes trafic between DSs, robots, FMS, APs, etc.
Model: Cisco Catalyst 3850

#### Todo
- Vlans:
    - 10-60: Red1-Blue3
    - 100: FMS network
    - 200: Venue Internet
- SVIs for each VLAN
- Trunks:
    - To red switch (10, 20, 30, 40, 50, 60, 100)
    - To blue switch (10, 20, 30, 40, 50)
    - To FMS AP (100, 200)
    - To robot AP (10, 20, 30, 40, 50, 60, 100)
- Routing:
    - Enabel IP routing
    - Set default route to venue internet gateway
- Access Control Lists (ACLs):
    - Block inter-VLAN between team VLANs (10-60)
    - Allow FMS VLAN (100) to access all VLANs
    - Allow DHCP, DNS, and NTP
    - Block internet except via venue internet VLAN (200) if enabled

### 1.2 Edge Switches
Purpose: Connect driverstations, isolate DSs via VLANs, and connect field end PLCs
Model: Cisco SG250-08

#### Todo
- Access Ports:
    - port 1: station 1 DS (10 for red, 40 for blue)
    - port 2: station 2 DS (20 for red, 50 for blue)
    - port 3: station 3 DS (30 for red, 60 for blue)
    - port 4: PLC (100)
- Trunk Port:
    - port 8: to core switch (10, 20, 30 or 40, 50, 60, and 100 (and 200 if internet enabled))
- Management IP on VLAN 100 (10.0.100.11 for red, 10.0.100.12 for blue)
- POE disabled on all ports

### 1.3 FMS Access Point
Purpose: Provide wireless access to FMS network & venue internet for field staff devices
Model: TBD

#### Todo
- SSID: cosmos-fms
- Static IP: 10.0.100.30

### 1.4 Robot Access Point
Purpose: Provide wireless access to robots
Model: VH-109 or VH-113

#### Todo
- Plug it in

## 2. FMS Server
### 2.1 Cosmos Application Network Side
Purpose: Core control for assigning teams, coordinating networking, and logging

#### Todo
- Network assignment manager (pushing configs to switches, APs, etc)
- PLC integration
- Logging system

### 2.2 DNS/NTP Server
Purpose: Provide DNS and NTP services to all devices on the FMS network

#### Todo
- dnsmasq forward to 1.1.1.1 or upstream DNS
- NTP server (can be dnsmasq or chrony)
- Add local DNS entries for field devices

## 3. "PLCs"
Purpose: Control field elements (lights, sounds, etc) and read field sensors (E-Stops, A-Stops, etc)
Model: Raspberry Pi

#### Todo
- Static IPs:
    - Core PLC: 10.0.100.20
    - Red PLC: 10.0.100.21
    - Blue PLC: 10.0.100.22

## 4. Venue Internet
Purpose: Provide internet access to FMS and field staff devices, and DSs when enabled

#### Todo
- SVI on core switch (200) -> 10.0.200.1/24
- NAT or routing to venue uplink gateway
- VLAN 200 trunk to FMS server and APs (tagged)
- ACLs to restrict internet access as needed

## 5. Automation
- VLAN assignment script for SVI IPs and DHCP ranges
- DHCP Confrig Builder
- Network Monitor
- Venue Internet toggle script