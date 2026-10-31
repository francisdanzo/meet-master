"""A pixel-dissolve transition constrained to the detected foreground."""

from __future__ import annotations

import time


class FrameTransition:
    """Dissolve only a foreground subject between a frozen and live frame."""

    def __init__(self, cv2, duration: float = 0.7, block_size: tuple[int, int] = (96, 54)):
        if duration <= 0:
            raise ValueError("la durée de transition doit être supérieure à zéro")
        self._cv2 = cv2
        self.duration = duration
        self._noise = None
        self._source = None
        self._started_at = 0.0
        self._block_size = block_size
        self._direction = "disappear"
        self._source_mask = None

    @property
    def active(self) -> bool:
        return self._source is not None

    @property
    def direction(self) -> str:
        return self._direction

    def start(
        self,
        source_frame,
        foreground_mask,
        direction: str,
        now: float | None = None,
    ) -> None:
        """Freeze the base image and begin a subject-only dissolve."""
        if direction not in {"disappear", "appear"}:
            raise ValueError("la direction doit être 'disappear' ou 'appear'")
        import numpy as np

        cv2 = self._cv2
        self._source = source_frame.copy()
        self._source_mask = foreground_mask.copy()
        self._direction = direction
        self._started_at = time.monotonic() if now is None else now
        cv2.setRNGSeed(42)
        self._noise = np.empty((self._block_size[1], self._block_size[0]), dtype=np.float32)
        cv2.randu(self._noise, 0.0, 1.0)

    def render(self, destination_frame, foreground_mask=None, now: float | None = None):
        """Return one frame with only the foreground subject dissolving."""
        if self._source is None:
            return destination_frame

        cv2 = self._cv2
        import numpy as np

        timestamp = time.monotonic() if now is None else now
        progress = min(1.0, max(0.0, (timestamp - self._started_at) / self.duration))
        # Ease in the disappearance, then let the last fragments clear quickly.
        eased = progress * progress * (3.0 - 2.0 * progress)
        height, width = destination_frame.shape[:2]
        noise = cv2.resize(self._noise, (width, height), interpolation=cv2.INTER_NEAREST)
        source = self._source
        if source.shape[:2] != destination_frame.shape[:2]:
            source = cv2.resize(source, (width, height), interpolation=cv2.INTER_LINEAR)

        if self._direction == "disappear":
            subject_mask = self._source_mask
            selection = cv2.compare(noise, eased, cv2.CMP_GE)
            output = destination_frame.copy()
            subject = source
        else:
            subject_mask = foreground_mask if foreground_mask is not None else self._source_mask
            selection = cv2.compare(noise, eased, cv2.CMP_LT)
            output = source.copy()
            subject = destination_frame

        if subject_mask.shape[:2] != (height, width):
            subject_mask = cv2.resize(
                subject_mask, (width, height), interpolation=cv2.INTER_LINEAR
            )
        selection = cv2.bitwise_and(selection, subject_mask)

        alpha = cv2.multiply(subject_mask, selection, scale=1.0 / 255.0)
        alpha_float = alpha.astype(np.float32)[:, :, None] / 255.0
        output = (
            subject.astype(np.float32) * alpha_float
            + output.astype(np.float32) * (1.0 - alpha_float)
        ).clip(0, 255).astype(np.uint8)

        # A narrow cyan-white fringe makes the moving mosaic boundary visible.
        if 0.04 < eased < 0.98:
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
            edge = cv2.morphologyEx(selection, cv2.MORPH_GRADIENT, kernel)
            glow = cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR)
            glow[:, :, 0] = edge
            glow[:, :, 1] = edge
            output = cv2.addWeighted(output, 1.0, glow, 0.48, 0)

        if progress >= 1.0:
            self._source = None
            self._noise = None
            self._source_mask = None
            return destination_frame
        return output
