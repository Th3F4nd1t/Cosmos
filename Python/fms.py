import threading
import time
import keyboard  # Install with `pip install keyboard`

import config as cfg
from field_ap import FieldAP
from driverstation import DriverStation

class FMS:
    def __init__(self):
        self.field_ap = FieldAP(cfg.FIELD_AP_IP)
        self.driverstations = [
            DriverStation(cfg.RED1_VLAN),
            DriverStation(cfg.RED2_VLAN),
            DriverStation(cfg.RED3_VLAN),
            DriverStation(cfg.BLUE1_VLAN),
            DriverStation(cfg.BLUE2_VLAN),
            DriverStation(cfg.BLUE3_VLAN)
        ]
        self.teams = [1, 2, 3, 4, 5, 6]
        self.teams_changed = False
        self.estops = [False] * 6
        self.is_estopped = False

        # Thread management
        self.threads = {}
        self.lock = threading.Lock()

        # Events
        self.field_estop_event = threading.Event()
        self.stop_event = threading.Event()  # Global stop event for clean thread exits

        # Match state
        self.match_state = {"state": "idle", "time_remaining": 0}

    def log(self, message):
        print(f"[FMS] {message}")

    def run(self):
        """Main loop that ensures threads are spawned and running."""
        self.log("Welcome to COSMOS Field Management System!")
        self.log(f"Field AP is at IP: {cfg.FIELD_AP_IP}")

        for i in range(3):
            self.log(f"Red {i+1} VLAN: {self.driverstations[i].vlan}")
        for i in range(3):
            self.log(f"Blue {i+1} VLAN: {self.driverstations[i+3].vlan}")

        # Start required threads
        self.start_thread("connection", self.connection_thread_func)
        self.start_thread("safety", self.safety_thread_func)
        self.start_thread("keyboard", self.keyboard_listener)

        while not self.stop_event.is_set():
            with self.lock:
                if self.match_state["state"] == "running" and "match" not in self.threads:
                    self.start_thread("match", self.match_thread_func)
            time.sleep(1)  # Prevent CPU overuse

    def start_thread(self, name, target, *args):
        """Starts and tracks a new thread if not already running."""
        if name in self.threads:
            return
        thread = threading.Thread(target=target, args=args, name=name, daemon=True)
        thread.start()
        self.threads[name] = thread
        self.log(f"Started thread: {name}")

    def stop_all_threads(self):
        """Stops all running threads safely."""
        self.log("Stopping all threads...")
        self.stop_event.set()  # Signal threads to exit
        with self.lock:
            for name, thread in list(self.threads.items()):
                self.log(f"Waiting for thread {name} to exit...")
                thread.join(timeout=2)  # Give threads a chance to stop
                self.threads.pop(name)
        self.log("All threads stopped.")

    def shutdown_all_robots(self):
        """Disables all robots (sends a shutdown command)."""
        self.log("Disabling all robots!")
        try:
            for ds in self.driverstations:
                ds.estop()
            time.sleep(1)
            for ds in self.driverstations:
                if ds.get_status()["isRobotRunning"]:
                    self.log(f"Failed to disable robot {ds.vlan}.")
                else:
                    self.log(f"Disabled robot {ds.vlan}.")
        except Exception as e:
            self.log(f"Error disabling robots: {e}")

    def connection_thread_func(self):
        """Scans for Driver Stations and updates their status."""
        while not self.stop_event.is_set():
            self.log("Scanning for devices...")
            for ds in self.driverstations:
                ds.check_connection()
            time.sleep(5)

    def safety_thread_func(self):
        """Monitors E-Stops and stops everything when triggered."""
        while not self.stop_event.is_set():
            if self.field_estop_event.is_set():
                self.log("🚨 EMERGENCY STOP ACTIVATED! 🚨")
                with self.lock:
                    self.match_state["state"] = "stopped"
                    self.shutdown_all_robots()
                    self.stop_all_threads()
                self.field_estop_event.clear()
            time.sleep(1)

    def keyboard_listener(self):
        """Listens for keyboard input and triggers E-Stop when SPACE is pressed."""
        self.log("Keyboard listener started. Press SPACE to trigger E-Stop.")
        while not self.stop_event.is_set():
            keyboard.wait("space")  # Blocks until space is pressed
            self.log("🚨 SPACE PRESSED! TRIGGERING E-STOP! 🚨")
            self.field_estop_event.set()
            self.stop_all_threads()
            time.sleep(0.5)  # Prevent multiple triggers in quick succession

    def match_thread_func(self):
        """Handles the match state and spawns robot threads."""
        self.log("Starting match...")
        self.match_state["state"] = "running"
        self.match_state["time_remaining"] = 150

        for i, ds in enumerate(self.driverstations):
            self.start_thread(f"robot-{i}", self.robot_thread_func, ds)

        while self.match_state["state"] == "running" and not self.stop_event.is_set():
            self.log(f"Match in progress... {self.match_state['time_remaining']}s left")
            time.sleep(1)
            with self.lock:
                self.match_state["time_remaining"] -= 1
                if self.match_state["time_remaining"] <= 0:
                    self.match_state["state"] = "ending"

        self.log("Match ending...")
        with self.lock:
            self.match_state["state"] = "idle"
            self.stop_all_threads()

    def robot_thread_func(self, ds):
        """Handles a single robot during a match."""
        self.log(f"Robot {ds.vlan} is active.")
        while self.match_state["state"] == "running" and not self.stop_event.is_set():
            ds.send_match_signal("running")
            time.sleep(2)
        self.log(f"Robot {ds.vlan} is stopping.")
