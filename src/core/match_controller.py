import logging
import time
import threading

from core.state_store import States
from tools.terminal.decorators import user_run

logger = logging.getLogger("match_controller")


class MatchController:
    @user_run
    def __init__(self, fms):
        self.fms = fms
        self.number = self.fms.state_store.state["match"]["number"]
        self.teams = self.fms.state_store.state["teams"].keys()
        self.progression = self.fms.state_store.state["match"]["progression"]

    @user_run
    def start_match(self, instance_id: int | None = None):
        threading.Thread(target=self._start_match).start()
        logger.debug("Match started")
        # Emit event to start match
        self.fms.event_bus.emit("match_started", {"number": self.number, "teams": self.teams})
        # Wait for match to finish

    @user_run
    def _start_match(self, instance_id: int | None = None):
        if self.fms.state_store.get_state() != States.MATCH_PRE:
            logger.error("Match cannot be started, not in MATCH_PRE state")
            self.fms.event_bus.emit("match_error", {"error": "Match cannot be started, not in MATCH_PRE state"})
            return

        for pose in self.progression:
            expected_duration = pose[1]
            self.fms.state_store.set_state(pose[0])
            self.fms.state_store.state["match"]["time_left"] = expected_duration

            logger.info(f"Setting state to {pose[0]} with duration {expected_duration:.2f}s")
            # Special handling for MATCH_POST
            if self.fms.state_store.get_state() == States.MATCH_POST:
                logger.debug("Match is in post phase, waiting for user input")
                idn = self.fms.user_attention.add("Match is in post phase, waiting for greenlight", ["Greenlight"])
                while self.fms.user_attention.get(idn)[3] is None:
                    time.sleep(0.1)
                match self.fms.user_attention.get(idn)[3]:
                    case 0:
                        logger.info("Greenlight received, switching to MATCH_GREENLIGHT")
                        self.fms.state_store.set_state(States.MATCH_GREENLIGHT)
                        self.fms.user_attention.remove(idn)
                        return

            # Accurate timing loop
            start_time = time.perf_counter()
            time_left = expected_duration

            while time_left > 0:
                time.sleep(0.05)
                elapsed = time.perf_counter() - start_time
                time_left = expected_duration - elapsed
                self.fms.state_store.state["match"]["time_left"] = max(0, time_left)

            # Timing debug
            actual_duration = time.perf_counter() - start_time
            logger.debug(f"State {pose[0]} expected duration: {expected_duration:.2f}s, actual: {actual_duration:.2f}s")

            # State mismatch check
            if self.fms.state_store.get_state() != pose[0]:
                logger.error(f"State mismatch: {self.fms.state_store.get_state()} != {pose[0]}")
                self._handle_state_mismatch(instance_id)

    @user_run
    def _handle_state_mismatch(self, instance_id: int | None = None):
        if self.fms.state_store.get_state() == States.MATCH_ABORT_OR_ESTOP:
            logger.error("Match aborted or field estop triggered")
        elif self.fms.state_store.get_state() == States.CRASHED:
            logger.error("Match crashed")