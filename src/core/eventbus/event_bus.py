import logging
import threading
from collections import defaultdict
from typing import Callable, Dict, Any, List, Optional
from queue import Queue, Empty
import time
from core.eventbus.events import GeneralEvent, EventBusEvent, MatchEvent, RobotEvent, PLCEvent, StateEvent, SwitchEvent, TeamEvent, UserAttentionEvent, TerminalEvent

from tools.terminal.decorators import system_run


class EventBus:
    @system_run
    def __init__(self):
        self._subscribers: Dict[str, List[Callable[[Any], None]]] = defaultdict(list)
        self._queue: Queue = Queue()
        self._lock = threading.Lock()
        self._condition = threading.Condition()
        self._running = False
        self._thread = None
        
    @system_run
    def subscribe(self, event_type: GeneralEvent|EventBusEvent|MatchEvent|RobotEvent|PLCEvent|StateEvent|SwitchEvent|TeamEvent|UserAttentionEvent|TerminalEvent, callback: Callable[[Any], None]):
        """
        Register a callback for a specific event type.
        Thread-safe.
        """
        with self._lock:
            self.emit(EventBusEvent.SUBSCRIBED, {"event_type": event_type, "callback": callback.__name__})
            if event_type == "*":
                # Special case for wildcard subscription
                for key in self._subscribers:
                    if callback not in self._subscribers[key]:
                        self._subscribers[key].append(callback)
                return

            if event_type not in self._subscribers:
                self._subscribers[event_type] = []
            if callback in self._subscribers[event_type]:
                self.emit(EventBusEvent.WARNING, {"warning": f"Callback {callback.__name__} already subscribed to event {event_type.name_str}"})
                return
            self._subscribers[event_type].append(callback)

    def unsubscribe(self, event_type: GeneralEvent|EventBusEvent|MatchEvent|RobotEvent|PLCEvent|StateEvent|SwitchEvent|TeamEvent|UserAttentionEvent|TerminalEvent, callback: Callable[[Any], None]):
        """
        Unregister a callback for a specific event type.
        Thread-safe.
        """
        with self._lock:
            if event_type in self._subscribers:
                try:
                    self._subscribers[event_type].remove(callback)
                    self.emit(EventBusEvent.UNSUBSCRIBED, {"event_type": event_type, "callback": callback.__name__})
                except ValueError:
                    self.emit(EventBusEvent.WARNING, {"warning": f"Callback {callback.__name__} not found for event {event_type.name_str}"})
            else:
                self.emit(EventBusEvent.WARNING, {"warning": f"No subscribers for event: {event_type.name_str}"})

    @system_run
    def emit(self, event_type: GeneralEvent|EventBusEvent|MatchEvent|RobotEvent|PLCEvent|StateEvent|SwitchEvent|TeamEvent|UserAttentionEvent|TerminalEvent, data: dict = None):
        """
        Emit an event to all subscribers.
        Thread-safe.
        """

        # Validate the event type with the payload
        if not event_type.validate(data):
            self.emit(EventBusEvent.ERROR, {"error": f"Invalid data for event {event_type.name_str}: {data}"})
            return

        self._queue.put((event_type, data))
        with self._condition:
            self._condition.notify_all()

    @system_run
    def run(self):
        """
        Starts the event loop in a dedicated thread.
        Call this once.
        """
        if self._running:
            self.emit(EventBusEvent.WARNING, {"warning": "EventBus is already running"})
            return

        self._running = True
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()
        self.emit(GeneralEvent.INFO, {"message": "EventBus started"})

    @system_run
    def _run_loop(self):
        while self._running:
            try:
                event_type, data = self._queue.get(timeout=0.1)
            except Empty:
                continue

            with self._lock:
                callbacks = self._subscribers.get(event_type, [])

            if not callbacks:
                self.emit(EventBusEvent.WARNING, {"warning": f"No subscribers for event: {event_type.name_str}"})
                continue

            for callback in callbacks:
                try:
                    callback(data)
                except Exception as e:
                    self.emit(EventBusEvent.ERROR, {"error": f"Error in callback for {event_type.name_str}: {e}"})

    @system_run
    def wait_for(self, event_type: GeneralEvent|EventBusEvent|MatchEvent|RobotEvent|PLCEvent|StateEvent|SwitchEvent|TeamEvent|UserAttentionEvent|TerminalEvent, check: Callable[[Any], bool] = lambda _: True, timeout: float = None) -> Optional[Any]:
        """
        Waits for a specific event to occur that passes the check function.
        Blocks the calling thread.
        """
        result = [None]

        def _callback(data):
            if check(data):
                with self._condition:
                    result[0] = data
                    self._condition.notify_all()

        self.subscribe(event_type, _callback)

        start_time = time.time()
        with self._condition:
            while result[0] is None:
                remaining = None
                if timeout is not None:
                    elapsed = time.time() - start_time
                    remaining = timeout - elapsed
                    if remaining <= 0:
                        break
                self._condition.wait(timeout=remaining)

        if result[0] is None:
            self.emit(EventBusEvent.WARNING, {"warning": f"Timeout waiting for event: {event_type.name_str}"})
        return result[0]

    @system_run
    def stop(self):
        """
        Stops the event loop.
        """
        self._running = False
        self.emit(GeneralEvent.INFO, {"message": "EventBus stopped"})
