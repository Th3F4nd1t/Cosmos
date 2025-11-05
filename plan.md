# Project Requirements

This document outlines what the requirements of Cosmos FMS are by the time it's completed to keep development on track.

## Physical
- Must fit in a field
- Must be transportable by 1-2 people
- Must be able to run off of field power (120V 15A)

## Team Interaction
- Must have E-Stops and A-Stops for each driverstation
- Must have a form of field E-Stop
- Must have number panels for each driverstation

## Network
- Must use proper and isolated VLANs per team
- Must be able to connect to all robots
- Must be able to connect to all driverstations
- Must have a wireless AP for access to webserver
- Must have switches under the driverstations powered by POE

## Web Interface
- Must show match time
- Must show team information
- Must show robot status
- Must show driverstation status
- Must show field status
- Must show logs
- Must allow starting/stopping matches
- Must allow changing field states
- Must allow enabling/disabling robots
- Must allow viewing/changing settings
- Must have role-based access control
- Must be accessible over wireless

## Matches
- Must be able to run standard matches (2:30)
- Must be able to handle interaction with auto-scorers optionally and also hand scoring
- Must be able to automate switching of match modes
- Must be able to log match data for later review

## Normal Use
- Must be able to enable/disable robots
- Must be able to log data continuously
- Must be able to allow driverstations to connect to robots and also the internet
- Must have a remote "terminal" to allow for commands to be run

## Show Modes
- Must have a demo mode for showcasing the field
- Must have a diagnostics mode for troubleshooting issues
- Must have control over light panels RGB values



# Implementation

## Hurdles:
- How to move between states cleanly?
- How to structure interaction from states?
- How to interact with PLCs?
- How to interact with network devices?
- How to interact with driverstations?
- How to communicate with various terminals, doing user input requests, etc.?
- How to structure logging?
- How to structure webserver and API?
- How to structure role-based access control?