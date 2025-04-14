from thread_handler import ThreadHandler

class Event:
    """
    Class representing an event. An event can be started, stopped, and updated. It can also have a start condition and a stop condition.
    """
    def __init__(self, name, start_condition=None, stop_condition=None):
        self.name = name

        self.start_condition = start_condition
        self.stop_condition = stop_condition

        self.is_running = False

        self._thread_handler = ThreadHandler()
        self.next_thread_name = "thread_0"



    def add_dependent(self, event: callable):
        """
        Add a dependent event to this event. A dependent event will be started when this event is started.
        """

        self._thread_handler.create_thread(str(self.next_thread_name), event)

        self.next_thread_name = f"thread_{int(self.next_thread_name.split('_')[1]) + 1}"



    def start(self):
        """
        Start the event. This will also start all dependent events.
        """
        self._thread_handler.start_all_threads()



    def stop(self):
        """
        Stop the event. This will also stop all dependent events.
        """
        self._thread_handler.stop_all_threads()



class EventHandler:
    """
    Class to handle events and host an event queue as well as the decorators to add to said event queue as well as add dependents to an event.
    """
    def __init__(self):
        self.events = {}

    

    def register_event(self, event: Event):
        """
        Add an event to the event queue.
        """
        self.events[event.name] = event

        return event.name
    


    def on_event(self, event_name: str):
        """
        Decorator to add an event to the event queue.
        """
        def decorator(func):
            if event_name not in self.events:
                raise Exception(f"Event {event_name} does not exist.")

            self.events[event_name].add_dependent(func)

            return func

        return decorator