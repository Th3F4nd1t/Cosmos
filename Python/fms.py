import time
import traceback
from logger import Logger
from thread_handler import ThreadHandler
from shell import CommandContext, shell_loop
from ds import DriverStation, DriverStationMode, DriverStationMatchType, Station
import random
from collections import defaultdict
from flask import Flask, jsonify, request

class FMSState:
    WAITING = 0

class FMS:
    def __init__(self):
        self.logger = Logger()
        self.thread_handler = None
        self.isStarted = False

        self.matches = []
        self.ds_map = {
            "9991" : Station.RED1,
            "9992" : Station.RED2,
            "9993" : Station.RED3,
            "9994" : Station.BLUE1,
            "9995" : Station.BLUE2,
            "9996" : Station.BLUE3
        }

        self.set_pin()

    def set_pin(self):
        while True:
            self.pin = input("Create control pin: ")
            if self.pin.isdigit() and len(self.pin) >= 4:
                self.pin = int(self.pin)
                break
            else:
                self.logger.log("Invalid control pin. Must be at least 4 digits.", Logger.LogLevel.WARNING)

        self.logger.log(f"Control pin set to {self.pin}.", Logger.LogLevel.INFO)
        self.logger.log(f"DO NOT SHARE THIS PIN WITH ANYONE WHO IS NOT APPROVED TO CONTROL THE FMS.", Logger.LogLevel.WARNING)


    def requires_fms(func):
        def wrapper(self, *args, **kwargs):
            if not self.isStarted:
                self.logger.log("FMS not started. Please start FMS first.", Logger.LogLevel.WARNING)
                return
            return func(self, *args, **kwargs)
        return wrapper
    
    def requires_pin(func):
        def wrapper(self, *args, **kwargs):
            if not self.pin:
                self.logger.log("Control pin not set. Please set control pin first.", Logger.LogLevel.WARNING)
                return
            input_pin = input("Enter control pin: ")
            if input_pin != str(self.pin):
                self.logger.log("Invalid control pin. Please try again.", Logger.LogLevel.WARNING)
                return
            return func(self, *args, **kwargs)
        return wrapper


    def main(self):
        root = CommandContext("")

        # Root commands
        for name, func in {
            "start": self.start_fms,
            "stop": self.stop_fms,
            "reload": self.reload_fms,
            "status": self.status_fms,
            "help": self.help,
            "end" : self.end
        }.items():
            root.add_command(name, func)


        # Match commands
        match_ctx = CommandContext("match")
        for name, func in {
            "prestart": self.prestart_match,
            "start": self.start_match,
            "greenlight": self.greenlight_match,
            "replay": self.replay_match,
            "show": self.show_matches
        }.items():
            match_ctx.add_command(name, func)

        match_populate_ctx = CommandContext("populate")
        for name, func in {
            "random": self.populate_random_matches,
            "teams": self.populate_teams,
            "file": self.populate_file
        }.items():
            match_populate_ctx.add_command(name, func)

        match_ctx.add_command("populate", match_populate_ctx)
        root.add_command("match", match_ctx)


        # Team commands
        team_ctx = CommandContext("team")
        for name, func in {
            "add": self.add_team,
            "remove": self.remove_team,
            "red1": self.red1_team,
            "red2": self.red2_team,
            "red3": self.red3_team,
            "blue1": self.blue1_team,
            "blue2": self.blue2_team,
            "blue3": self.blue3_team,
            "swap": self.swap_teams,
            "clear": self.clear_teams,
            "clearall": self.clear_all_teams,
            "enable": self.enable_teams,
            "disable": self.disable_teams
        }.items():
            team_ctx.add_command(name, func)

        root.add_command("team", team_ctx)


        # PLC commands
        plc_ctx = CommandContext("plc")
        for name, func in {
            "estop": self.plc_estop,
            "astop": self.plc_astop
        }.items():
            plc_ctx.add_command(name, func)

        plc_panel_ctx = CommandContext("panel")
        for name, func in {
            "update": self.plc_panel_update,
            "reset": self.plc_panel_reset,
            "color": self.plc_panel_color
        }.items():
            plc_panel_ctx.add_command(name, func)

        plc_ctx.add_command("panel", plc_panel_ctx)
        root.add_command("plc", plc_ctx)


        # AP commands
        ap_ctx = CommandContext("ap")
        for name, func in {
            "update": self.ap_update,
            "reset": self.ap_reset,
            "status": self.ap_status
        }.items():
            ap_ctx.add_command(name, func)

        root.add_command("ap", ap_ctx)


        # Log commands
        log_ctx = CommandContext("log")
        for name, func in {
            "level": self.log_level,
            "file": self.log_file
        }.items():
            log_ctx.add_command(name, func)

        root.add_command("log", log_ctx)


        # Debug commands
        debug_ctx = CommandContext("debug")
        debug_thread_ctx = CommandContext("thread")
        for name, func in {
            "start": self.debug_thread_start,
            "stop": self.debug_thread_stop,
            "status": self.debug_thread_status,
            "list": self.debug_thread_list
        }.items():
            debug_thread_ctx.add_command(name, func)

        debug_ctx.add_command("thread", debug_thread_ctx)
        root.add_command("debug", debug_ctx)

        self.logger.log("Commands loaded", Logger.LogLevel.DEBUG)

        # Shell loop
        c = shell_loop(root, self)

        return c


    # Command functions

    @requires_pin
    def start_fms(self, cmd):
        self.logger.log("Starting FMS", Logger.LogLevel.INFO)

        # Thread handler creation
        self.thread_handler = ThreadHandler()
        self.logger.log("Thread handler created", Logger.LogLevel.DEBUG)

        # Create threads for driver stations
        self.thread_handler.create_thread("ds_red_1", self.driver_station_target, Station.RED1, 9991)
        self.thread_handler.create_thread("ds_red_2", self.driver_station_target, Station.RED2, 9992)
        self.thread_handler.create_thread("ds_red_3", self.driver_station_target, Station.RED3, 9993)

        self.thread_handler.create_thread("ds_blue_1", self.driver_station_target, Station.BLUE1, 9994)
        self.thread_handler.create_thread("ds_blue_2", self.driver_station_target, Station.BLUE2, 9995)
        self.thread_handler.create_thread("ds_blue_3", self.driver_station_target, Station.BLUE3, 9996)

        self.logger.log("Driver station threads created", Logger.LogLevel.DEBUG)


        # Create control thread
        self.thread_handler.create_thread("control", self.control_target)
        self.logger.log("Control thread created", Logger.LogLevel.DEBUG)

        # Create event handler thread
        self.thread_handler.create_thread("event_handler", self.event_handler_target)
        self.logger.log("Event handler thread created", Logger.LogLevel.DEBUG)

        # Create API thread
        self.thread_handler.create_thread("api", self.api_target)
        self.logger.log("API thread created", Logger.LogLevel.DEBUG)

        # Start all threads
        self.thread_handler.start_all_threads()
        self.logger.log("All threads started", Logger.LogLevel.DEBUG)

        
        self.logger.log("FMS started", Logger.LogLevel.INFO)
        self.isStarted = True

    @requires_fms
    @requires_pin
    def stop_fms(self, cmd):
        self.logger.log("Stopping FMS", Logger.LogLevel.INFO)

        # Stop all threads
        if self.isStarted:
            self.thread_handler.stop_all_threads()
            self.logger.log("All threads stopped", Logger.LogLevel.DEBUG)
        else:
            self.logger.log("FMS not started. Cannot stop no threads.", Logger.LogLevel.WARNING)

        self.logger.log("FMS stopped", Logger.LogLevel.INFO)

    @requires_fms
    @requires_pin
    def reload_fms(self, cmd):
        # reloads the specified thread. if no thread is specified, reloads all threads
        cmd = cmd[1]
        if len(cmd) == 0:
            self.logger.log("Reloading all threads", Logger.LogLevel.INFO)
            self.thread_handler.stop_all_threads()
            time.sleep(2)
            self.thread_handler.start_all_threads()
            self.logger.log("All threads reloaded", Logger.LogLevel.INFO)
            return
        else:
            for name in cmd:
                if name in self.thread_handler.threads:
                    self.logger.log(f"Reloading thread {name}", Logger.LogLevel.INFO)
                    self.thread_handler.stop_thread(name)
                    time.sleep(2)
                    self.thread_handler.start_thread(name)
                    self.logger.log(f"Thread {name} reloaded", Logger.LogLevel.INFO)
                else:
                    self.logger.log(f"Thread {name} does not exist or is not active", Logger.LogLevel.WARNING)

    @requires_fms
    def status_fms(self, cmd):
        ...

    def help(self, cmd):
        self.logger.log("command (example usage) | description")
        self.logger.log("start (start) | starts the threads of the FMS, beings attempting to connect to ds and plcs, begins tracking events")
        self.logger.log("stop (stop) | ends the threads of the fms, stops everything that 'start' begins")
        self.logger.log("reload (reload <thread_name>) stops then starts the provided thread, if none reloads all threads")


    @requires_pin
    def end(self, cmd):
        self.logger.log("FMS ended", Logger.LogLevel.INFO)
        return 1

    @requires_fms
    @requires_pin
    def prestart_match(self, cmd):
        # Configure the switch for FMS server -> DS vlanning based on IPs
        # Configure AP (set teaam numbers)
        # Set team numbers on screens
        # Check for E/A-stops, if engaged, alert and wait for release
        self.logger.log("Prestart match configuration complete", Logger.LogLevel.INFO)

        ...

    @requires_fms
    @requires_pin
    def start_match(self, cmd):

        self.logger.log("Auton started", Logger.LogLevel.IMPORTANT)


        self.logger.log("Teleop started", Logger.LogLevel.IMPORTANT)


        self.logger.log("Match ended", Logger.LogLevel.IMPORTANT)
        ...

    @requires_fms
    @requires_pin
    def greenlight_match(self, cmd):
        ...

    @requires_fms
    @requires_pin
    def replay_match(self, cmd):
        ...

    @requires_pin
    def populate_random_matches(self, cmd):
        ...

    @requires_pin
    def populate_teams(self, cmd):
        ...

    @requires_pin
    def populate_file(self, cmd):
        ...

    @requires_pin
    def add_team(self, cmd):
        ...

    @requires_pin
    def remove_team(self, cmd):
        ...

    @requires_fms
    @requires_pin
    def red1_team(self, cmd):
        ...

    @requires_fms
    @requires_pin
    def red2_team(self, cmd):   
        ...

    @requires_fms
    @requires_pin
    def red3_team(self, cmd):
        ...

    @requires_fms
    @requires_pin
    def blue1_team(self, cmd):
        ...

    @requires_fms
    @requires_pin
    def blue2_team(self, cmd):
        ...

    @requires_fms
    @requires_pin
    def blue3_team(self, cmd):
        ...

    @requires_fms
    @requires_pin
    def swap_teams(self, cmd):
        ...

    @requires_fms
    @requires_pin
    def clear_teams(self, cmd):
        ...

    @requires_fms
    @requires_pin
    def clear_all_teams(self, cmd):
        ...

    @requires_fms
    @requires_pin
    def enable_teams(self, cmd):
        if len(cmd[1]) < 1:
            self.logger.log("No teams specified, enabling all")
            
            self.thread_handler.get_thread("ds_red_1").ds.enable()
            self.thread_handler.get_thread("ds_red_2").ds.enable()
            self.thread_handler.get_thread("ds_red_3").ds.enable()
            self.thread_handler.get_thread("ds_blue_1").ds.enable()
            self.thread_handler.get_thread("ds_blue_2").ds.enable()
            self.thread_handler.get_thread("ds_blue_3").ds.enable()
            
            self.logger.log("All teams enabled", Logger.LogLevel.DEBUG)
            return
        
        cmd = cmd[1]
        for team in cmd:
            if team in self.ds_map.keys:
                if self.ds_map[team] == Station.RED1:
                    self.thread_handler.get_thread("ds_red_1").enable()
                elif self.ds_map[team] == Station.RED2:
                    self.thread_handler.get_thread("ds_red_2").enable()
                elif self.ds_map[team] == Station.RED3:
                    self.thread_handler.get_thread("ds_red_3").enable()
                elif self.ds_map[team] == Station.BLUE1:
                    self.thread_handler.get_thread("ds_blue_1").enable()
                elif self.ds_map[team] == Station.BLUE2:
                    self.thread_handler.get_thread("ds_blue_2").enable()
                elif self.ds_map[team] == Station.BLUE3:
                    self.thread_handler.get_thread("ds_blue_3").enable()
                self.logger.log(f"Team {team} enabled", Logger.LogLevel.DEBUG)
            else:
                self.logger.log(f"Team {team} not found on field, skipping", Logger.LogLevel.WARNING)

    @requires_fms
    @requires_pin
    def disable_teams(self, cmd):
        if len(cmd[1]) < 1:
            self.logger.log("No teams specified, disabling all")
            
            self.thread_handler.get_thread("ds_red_1").ds.disable()
            self.thread_handler.get_thread("ds_red_2").ds.disable()
            self.thread_handler.get_thread("ds_red_3").ds.disable()
            self.thread_handler.get_thread("ds_blue_1").ds.disable()
            self.thread_handler.get_thread("ds_blue_2").ds.disable()
            self.thread_handler.get_thread("ds_blue_3").ds.disable()
            
            self.logger.log("All teams disabled", Logger.LogLevel.DEBUG)
            return
        
        cmd = cmd[1]
        for team in cmd:
            if team in self.ds_map.keys():
                if self.ds_map[team] == Station.RED1:
                    self.thread_handler.get_thread("ds_red_1").disable()
                elif self.ds_map[team] == Station.RED2:
                    self.thread_handler.get_thread("ds_red_2").disable()
                elif self.ds_map[team] == Station.RED3:
                    self.thread_handler.get_thread("ds_red_3").disable()
                elif self.ds_map[team] == Station.BLUE1:
                    self.thread_handler.get_thread("ds_blue_1").disable()
                elif self.ds_map[team] == Station.BLUE2:
                    self.thread_handler.get_thread("ds_blue_2").disable()
                elif self.ds_map[team] == Station.BLUE3:
                    self.thread_handler.get_thread("ds_blue_3").disable()
                self.logger.log(f"Team {team} disabled", Logger.LogLevel.DEBUG)
            else:
                self.logger.log(f"Team {team} not found on field, skipping", Logger.LogLevel.WARNING)

    def plc_estop(self, cmd):
        ...

    def plc_astop(self, cmd):
        ...

    @requires_pin
    def plc_panel_update(self, cmd):
        ...

    @requires_pin
    def plc_panel_reset(self, cmd):
        ...

    def plc_panel_color(self, cmd):
        ...

    @requires_pin
    def ap_update(self, cmd):
        ...

    @requires_pin
    def ap_reset(self, cmd):
        ...

    def ap_status(self, cmd):
        ...

    @requires_fms
    @requires_pin
    def debug_thread_start(self, cmd):
        ...

    @requires_fms
    @requires_pin
    def debug_thread_stop(self, cmd):
        ...

    @requires_fms
    def debug_thread_status(self, cmd):
        ...

    @requires_fms
    def debug_thread_list(self, cmd):
        if self.thread_handler is None:
            self.logger.log("Thread handler not running", Logger.LogLevel.WARNING)
        else:
            self.logger.log("Active threads:", Logger.LogLevel.INFO)
            for name, thread in self.thread_handler.threads.items():
                self.logger.log(f"Thread {name}: {'Running' if thread.is_alive() else 'Stopped'}", Logger.LogLevel.INFO)

    @requires_pin
    def log_level(self, cmd):
        cmd = cmd[1]
        if len(cmd) < 1:
            self.logger.log("Log level not specified", Logger.LogLevel.WARNING)
            return

        level = cmd[0].upper()
        if level in Logger.LogLevel.__members__:
            self.logger.set_log_level(Logger.LogLevel[level])
            self.logger.log(f"Log level set to {level}", Logger.LogLevel.INFO)
        else:
            self.logger.log(f"Invalid log level: {level}", Logger.LogLevel.WARNING)

    @requires_pin
    def log_file(self, cmd):
        cmd = cmd[1]
        if len(cmd) < 1:
            self.logger.log("Log file not specified", Logger.LogLevel.WARNING)
            return

        log_file = cmd[1]
        self.logger.log_file = log_file
        self.logger.log(f"Log file set to {log_file}", Logger.LogLevel.INFO)
                    

    
    def show_matches(self, cmd):
        self.logger.log("Matches:", Logger.LogLevel.INFO)
        for i, match in enumerate(self.matches):
            red, blue = match
            self.logger.log(f"Match {i + 1}: Red: {red}, Blue: {blue}", Logger.LogLevel.INFO)
    


    # Thread functions
    def driver_station_target(self, station: Station, team: int):
        ds = DriverStation(team, station)


        next_time = time.time()
        while True:
            pass


    
    def control_target(self):
        # Control thread logic here
        # should hold state of fms
        self.state = FMSState.WAITING
        while True:
            if self.state == FMSState.WAITING:
                pass


    def event_handler_target(self):
        # Event handler logic here
        events = []
        while True:
            if events != []:
                # deal with events
                pass
            


    def api_target(self):
        # start a flask server
        app = Flask(__name__)

        # define API endpoints
        @app.route('/driverstations', methods=['GET'])
        def driverstations():
            driverstations = {
                "red1": "9991",
                "red2": "9992",
            }
            return jsonify(driverstations)

        # start the app
        app.run(host='10.0.100.5', port=5000)

if __name__ == "__main__":
    while True:
        try:
            fms = FMS()
            c = fms.main()
            if c == 1:
                fms.logger.log("FMS stopped by user", Logger.LogLevel.IMPORTANT)
                break
        except KeyboardInterrupt:
            fms.logger.log("FMS stopped by user", Logger.LogLevel.IMPORTANT)
            break
        except Exception as e:
            fms.logger.log("FMS hard crashed. All unsaved data lost.", Logger.LogLevel.ERROR)
            fms.logger.log(f"Error: {e}", Logger.LogLevel.ERROR)
            fms.logger.log(f"Traceback: {traceback.format_exc()}", Logger.LogLevel.DEBUG)
            fms.logger.log("Please report the above error to the developers and include your fms.log file.", Logger.LogLevel.WARNING)
            fms.logger.log("Restarting FMS in 5 seconds...", Logger.LogLevel.INFO)
            time.sleep(5)
            continue