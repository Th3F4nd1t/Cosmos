basically

states get made. states can be switched
event handler creates threads of all dependant functions on a `on_state(state)` or `while_state(state)` etc decorators
so basically its a state machine that then calls events that then call functions

this lets us have all the fms states and do various things using threading for each state and various parts of that state, start, during, end, switch from a specified state, etc.

slight rework:
Threads:
- red_1: All traffic to and from red 1 driverstation. Also holds states for red 1.
- red_2: All traffic to and from red 2 driverstation. Also holds states for red 2.
- red_3: All traffic to and from red 3 driverstation. Also holds states for red 3.
- blue_1: All traffic to and from blue 1 driverstation. Also holds states for blue 1.
- blue_2: All traffic to and from blue 2 driverstation. Also holds states for blue 2.
- blue_3: All traffic to and from blue 3 driverstation. Also holds states for blue 3.
- control: Main controller. Think of it like a dispatcher. All threads "talk" with this one.
- event_handler: Checks PLCs for estops, astops, as well as handles connection/disconnect events from the driverstations. Then sets the various things in the control thread.
- api: Handles API end points. This is how the user interfaces with the FMS.

The main program just starts all these threads and handles terminal commands. It can also reload threads which therefore re-imports the needed functions in a "reload" sense to keep certain things up while testing new code on other parts.


list of commands:

- start: starts the fms
- stop: stops the fms ([f] for forced)
- reload: [thread_name] reloads the specified thread. If no thread is specified, reloads all threads.
- status: [thread_name] shows the status of the specified thread. If no thread is specified, shows the status of all threads.
- exit: exits the program. This will stop all threads and exit the program.
- help: shows a list of commands and their descriptions.
- match:
    - prestart
    - start
    - greenlight
    - populate
        - random
        - teams [team1, team2, team3, team4, team5, team6]
        - file [file_name]
    - replay [match_number]
    - show [match_number] all matches if no match number is specified
- team:
    - add [team_number] 
    - remove [team_number]
    - red1 [team_number]
    - red2 [team_number]
    - red3 [team_number]
    - blue1 [team_number]
    - blue2 [team_number]
    - blue3 [team_number]
    - swap [ds_number] [ds_number]
    - clear [ds_number]
    - clear_all
- plc
    - estop [ds_number] [on/off]
    - astop [ds_number] [on/off]
    - estopall [on/off]
    - astopall [on/off]
    - panel
        - update
        - color [red/green/yellow/blue]
- ap
    - update
    - status
- log
    - level [level]
    - file [file_name]
