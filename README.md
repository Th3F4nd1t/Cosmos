# Cosmos

What will happen (kinda):
- Connect to Driver Stations
- Connect to Field AP
- Convice DS that they are on a FMS
- Tell Field AP which teams it should use
- Connect to fake PLCs
- Init buttons and light panels
- In init/test mode, have all e/a stops be activated
- After init/test mode, run a test match
- After test match, move to standby mode
- Upon instruction the system can move to either "Multi-bot", "Single-bot", or "Match" mode
- Multi-bot mode will allow for multiple robots to be controlled independantly
- Single-bot mode will allow for a single robot to be controlled
- Match mode will allow for a match to be run
- In multi-bot and single-bot mode, the system shouldn't make a DS think its attached to a FMS, only to the robot directly
- In match mode, the system should make the DS think its attached to a FMS



Cheesy Arena will be very helpful to figuring out the network side of how the fms will need to work to work with Driver stations.
Also the FMS doesn't talk to robots, instead it only talks to the DS, which then talks to the robot.
If the DS loses connection to the FMS, it will shut down the robot (hopefully)

To-Do:
- Talk to DS
    - Establish connection to DS
    - 
- Talk to Field AP
- Talk to PLCs