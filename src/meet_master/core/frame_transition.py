"""Small, reusable pixel-dissolve transition between two video frames."""

from __future__ import annotations

import time


class FrameTransition:
    """Dissolve a frozen source image into a changing destination image."""

    def __init__(self, cv2, duration: float = 0.7, block_size: tuple[int, int] = (96, 54)):
        if duration <= 0:
            raise ValueError("la durée de transition doit être supérieure à zéro")
        self._cv2 = cv2
        self.duration = duration
        self._noise = None
        self._source = None
        self._started_at = 0.0
        self._block_size = block_size

    @property
    def active(self) -> bool:
        return self._source is not None

    def start(self, source_frame, now: float | None = None) -> None:
        """Freeze the outgoing image and begin a dissolve from it."""
        import numpy as np

        cv2 = self._cv2
        self._source = source_frame.copy()
        self._started_at = time.monotonic() if now is None else now
        cv2.setRNGSeed(42)
        self._noise = np.empty((self._block_size[1], self._block_size[0]), dtype=np.float32)
        cv2.randu(self._noise, 0.0, 1.0)

    def render(self, destination_frame, now: float | None = None):
        """Return one dissolve frame; the destination may change every call."""
        if self._source is None:
            return destination_frame

        cv2 = self._cv2
        timestamp = time.monotonic() if now is None else now
        progress = min(1.0, max(0.0, (timestamp - self._started_at) / self.duration))
        # Ease in the disappearance, then let the last fragments clear quickly.
        eased = progress * progress * (3.0 - 2.0 * progress)
        height, width = destination_frame.shape[:2]
        noise = cv2.resize(self._noise, (width, height), interpolation=cv2.INTER_NEAREST)
        threshold = eased
        target_mask = cv2.compare(noise, threshold, cv2.CMP_LT)
        source_mask = cv2.bitwise_not(target_mask)

        source = self._source
        if source.shape[:2] != destination_frame.shape[:2]:
            source = cv2.resize(source, (width, height), interpolation=cv2.INTER_LINEAR)
        output = cv2.bitwise_or(
            cv2.bitwise_and(source, source, mask=source_mask),
            cv2.bitwise_and(destination_frame, destination_frame, mask=target_mask),
        )

        # A narrow cyan-white fringe makes the moving mosaic boundary visible.
        if 0.04 < eased < 0.98:
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
            edge = cv2.morphologyEx(target_mask, cv2.MORPH_GRADIENT, kernel)
            glow = cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR)
            glow[:, :, 0] = edge
            glow[:, :, 1] = edge
            output = cv2.addWeighted(output, 1.0, glow, 0.48, 0)

        if progress >= 1.0:
            self._source = None
            self._noise = None
            return destination_frame
        return output
