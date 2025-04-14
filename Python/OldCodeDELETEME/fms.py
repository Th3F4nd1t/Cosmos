import threading
from event import EventHandler, Event
from thread_handler import ThreadHandler


class FMS:
    #  sub classes
    # init function
    def __init__(self):
        """
        Variables to store all the parts of the Field state and the FMS state as well as all the connected devices.
        """
        # User defined variables
        self.debug = False

        # Thread Handler
        self.thread_handler = ThreadHandler()

        # Event Handler
        self.event_handler = EventHandler()

        # Driver Station

        # PLCs

        # API

        # State

        # Other

    def log(self, message: str, source: str = "FMS", level: str = "INFO"):
        """
        Log function to log messages to the console and to a file. This should be used for all logging in the FMS.
        """
        colors = {
            "DEBUG": "\033[94m",
            "INFO": "\033[92m",
            "WARNING": "\033[93m",
            "ERROR": "\033[91m",
            "CRITICAL": "\033[91m"
        }
        reset = "\033[0m"

        if level == "INFO" or (level == "DEBUG" and self.debug) or level == "WARNING" or level == "ERROR" or level == "CRITICAL":
            print(f"{colors.get(level, reset)}[{source}]: {message} {reset}")

        with open("fms.log", "a") as f:
            f.write(f"[{level} - {source}]: {message}\n")
            f.flush()



    def run(self):
        """
        Main function to start the FMS.
        """
        self.log("Starting FMS...", source="FMS", level="INFO")

        # Loop that checks event triggers. If an event is triggered, spawn threads for all dependants.
        while True:
            for event in self.event_handler.events.values():
                if event.start_condition and not event.is_running:
                    self.event_handler.start_event(event.name)
                    event.is_running = True




if __name__ == "__main__":
    fms = FMS()
    fms.rainbow_log()