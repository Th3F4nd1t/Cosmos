from enum import Enum
from tools.terminal.decorators import user_run, system_run


#### Shell Instance and Handler Classes ####
class MessageLevel(Enum):
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3


class ShellInstance:
    def __init__(self, instance_id:int):
        self.instance_id = instance_id
        self.messages = []

    def send_message(self, message:str, level:MessageLevel):
        self.messages.append((message, level))
        print(f"[{self.instance_id}] {level.name}: {message}")


class ShellHandler:
    def __init__(self, fms):
        self.fms = fms
        self.instances:dict[int, ShellInstance] = {}
    
    def broadcast(self, message:str, level:MessageLevel):
        for instance in self.instances.values():
            instance.send_message(message, level)
        print(f"[BROADCAST] {level.name}: {message}")

    def send_message(self, instance_id:int, message:str, level:MessageLevel):
        if instance_id in self.instances:
            self.instances[instance_id].send_message(message, level)
        else:
            self.broadcast(f"Instance {instance_id} not found but a message was attempted to be sent.", MessageLevel.ERROR)

    def check_instance(self, instance_id:int|None):
        if instance_id is None or instance_id not in self.instances:
            raise RuntimeError(f"Instance {instance_id} does not exist or is not valid.")
        return self.instances[instance_id]


if __name__ == "__main__":
    # testing code
    handler = ShellHandler(None)
    handler.broadcast("System is starting up.", MessageLevel.INFO)

    @user_run
    def example_user_run(instance_id):
        handler.send_message(instance_id, "User command executed.", MessageLevel.INFO)

    @user_run
    def another_user_run(instance_id):
        handler.send_message(instance_id, "Another user command executed.", MessageLevel.DEBUG)

    @system_run
    def example_system_run():
        handler.broadcast("System run executed.", MessageLevel.INFO)

    @system_run
    def bad_system_run(instance_id):
        handler.send_message(instance_id, "Another user command executed.", MessageLevel.DEBUG)

    @system_run
    def half_bad_system_run():
        handler.send_message(1, "This should fail because it has an instance_id.", MessageLevel.WARNING)

    # call the functions
    instance = ShellInstance(1)
    handler.instances[1] = instance
    example_user_run(1)
    example_system_run()
    try:
        bad_system_run(1)  # This should raise an error
    except RuntimeError as e:
        print(e)
    try:
        half_bad_system_run()  # This should also raise an error
    except TypeError as e:
        print(e)
    handler.send_message(1, "This is a test message.", MessageLevel.DEBUG)
    handler.broadcast("This is a broadcast message.", MessageLevel.INFO)