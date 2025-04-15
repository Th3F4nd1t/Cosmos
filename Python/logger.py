from enum import Enum


class Logger:
    class LogLevel(Enum):
            DEBUG = 0
            INFO = 1
            WARNING = 2
            IMPORTANT = 3
            ERROR = 4
            

    def __init__(self, log_file='fms.log'):
        self.log_file = log_file
        self.log_show_level = self.LogLevel.DEBUG


    def set_log_level(self, level: LogLevel):
        """
        Set the log level for the logger. The log level can be one of the following:
        - DEBUG
        - INFO
        - WARNING
        - ERROR
        - IMPORTANT
        """
        self.log_show_level = level
    

    def log(self, message: str, level: LogLevel = LogLevel.INFO):
        """
        Log a message to the log file and to the console.
        """
        if level.value >= self.log_show_level.value:
            if level == self.LogLevel.ERROR:
                print(f"\033[91m[{level.name}] {message}\033[0m")
            elif level == self.LogLevel.WARNING:
                print(f"\033[93m[{level.name}] {message}\033[0m")
            elif level == self.LogLevel.IMPORTANT:
                print(f"\033[94m[{level.name}] {message}\033[0m")
            else:
                print(f"[{level.name}] {message}")

        with open(self.log_file, 'a') as f:
            f.write(f"[{level.name}] {message}\n")