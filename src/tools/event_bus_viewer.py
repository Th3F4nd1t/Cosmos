import time
from core.event_bus import EventBus


def event_bus_viewer(event_bus: EventBus):
    """
    A simple viewer for the EventBus that prints events as they are emitted.
    """
    def event_handler(event_type: str, data: dict):
        print(f"Event: {event_type}, Data: {data}")

    # Subscribe to all events
    event_bus.subscribe("*", event_handler)

    try:
        print("EventBus Viewer started. Press Ctrl+C to exit.")
        while True:
            time.sleep(1)  # Keep the viewer running
    except KeyboardInterrupt:
        print("EventBus Viewer stopped.")
    finally:
        event_bus.unsubscribe("*", event_handler)  # Clean up subscription