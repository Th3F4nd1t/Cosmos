import logging
import threading
from collections import defaultdict
from typing import Callable, Dict, Any, List, Optional
from queue import Queue, Empty
import time

logger = logging.getLogger("event_bus")

class EventBus:
    def __init__(self):
        self._subscribers: Dict[str, List[Callable[[Any], None]]] = defaultdict(list)
        self._queue: Queue = Queue()
        self._lock = threading.Lock()
        self._condition = threading.Condition()
        self._running = False
        self._thread = None

    def subscribe(self, event_type: str, callback: Callable[[Any], None]):
        """
        Register a callback for a specific event type.
        Thread-safe.
        """
        with self._lock:
            logger.debug(f"Subscribed to {event_type}: {callback.__name__}")
            self._subscribers[event_type].append(callback)

    def emit(self, event_type: str, data: dict = None):
        """
        Emit an event to all subscribers.
        Thread-safe.
        """
        logger.debug(f"Emitting event {event_type} with data: {data}")
        self._queue.put((event_type, data))
        with self._condition:
            self._condition.notify_all()

    def run(self):
        """
        Starts the event loop in a dedicated thread.
        Call this once.
        """
        if self._running:
            logger.warning("EventBus is already running")
            return

        self._running = True
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()
        logger.info("EventBus thread started")

    def _run_loop(self):
        while self._running:
            try:
                event_type, data = self._queue.get(timeout=0.1)
            except Empty:
                continue

            with self._lock:
                callbacks = self._subscribers.get(event_type, [])

            if not callbacks:
                logger.warning(f"No subscribers for event: {event_type}")
                continue

            for callback in callbacks:
                try:
                    callback(data)
                except Exception as e:
                    logger.error(f"Error in callback for {event_type}: {e}")

    def wait_for(self, event_type: str, check: Callable[[Any], bool] = lambda _: True, timeout: float = None) -> Optional[Any]:
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
            logger.warning(f"Timeout waiting for event: {event_type}")
        return result[0]

    def stop(self):
        """
        Stops the event loop.
        """
        self._running = False
        logger.info("EventBus stopped")
