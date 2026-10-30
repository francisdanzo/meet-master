"""Presence state toggled by a confirmed Victory/V hand sign."""

from __future__ import annotations

from enum import Enum
import time

from meet_master.core.gesture_recognizer import GestureObservation


class PresenceState(str, Enum):
    """Whether the local preview should show the live camera or absence card."""

    PRESENT = "present"
    AWAY = "away"


class PresenceController:
    """Toggle presence with one debounced V sign, then wait for its release.

    A V sign must remain recognized for ``hold_seconds`` before it toggles the
    state. The controller will not accept another V sign until the current sign
    has been absent for ``release_seconds``. This prevents one held pose or
    short recognition flicker from toggling repeatedly.
    """

    def __init__(self, hold_seconds: float = 0.35, release_seconds: float = 0.25):
        if hold_seconds < 0 or release_seconds < 0:
            raise ValueError("les durées de confirmation doivent être positives ou nulles")
        self.hold_seconds = hold_seconds
        self.release_seconds = release_seconds
        self.state = PresenceState.PRESENT
        self._gesture_started_at: float | None = None
        self._release_started_at: float | None = None
        self._latched = False

    def update(self, observation: GestureObservation, now: float | None = None) -> PresenceState | None:
        """Update from one frame and return the new state only when it changes."""
        timestamp = time.monotonic() if now is None else now
        victory_detected = any(hand.gesture == "Victory" for hand in observation.hands)

        if victory_detected:
            self._release_started_at = None
            if self._latched:
                return None
            if self._gesture_started_at is None:
                self._gesture_started_at = timestamp
                return None
            if timestamp - self._gesture_started_at < self.hold_seconds:
                return None

            self.state = (
                PresenceState.AWAY
                if self.state is PresenceState.PRESENT
                else PresenceState.PRESENT
            )
            self._latched = True
            self._gesture_started_at = None
            return self.state

        self._gesture_started_at = None
        if self._latched:
            if self._release_started_at is None:
                self._release_started_at = timestamp
            elif timestamp - self._release_started_at >= self.release_seconds:
                self._latched = False
                self._release_started_at = None
        return None
