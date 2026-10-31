"""Foreground silhouette estimation by comparing frames to a clean plate."""

from __future__ import annotations


class ForegroundSegmenter:
    """Build a soft foreground mask from the startup background reference."""

    def __init__(self, cv2, background_reference, threshold: int = 28):
        if not 0 <= threshold <= 255:
            raise ValueError("le seuil de segmentation doit être compris entre 0 et 255")
        self._cv2 = cv2
        self._background = background_reference.copy()
        self.threshold = threshold

    def mask(self, frame):
        """Return a feathered 8-bit mask for the largest changed region."""
        cv2 = self._cv2
        reference = self._background
        reference_size = (reference.shape[1], reference.shape[0])
        scaled = cv2.resize(frame, reference_size, interpolation=cv2.INTER_AREA)
        difference = cv2.absdiff(scaled, reference)
        channels = cv2.split(difference)
        strongest = cv2.max(cv2.max(channels[0], channels[1]), channels[2])
        strongest = cv2.GaussianBlur(strongest, (5, 5), 0)
        _, binary = cv2.threshold(strongest, self.threshold, 255, cv2.THRESH_BINARY)

        close_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
        open_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, close_kernel)
        binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, open_kernel)

        count, labels, stats, _ = cv2.connectedComponentsWithStats(binary, connectivity=8)
        minimum_area = max(24, round(binary.shape[0] * binary.shape[1] * 0.004))
        candidates = [
            index
            for index in range(1, count)
            if minimum_area <= stats[index, cv2.CC_STAT_AREA] <= binary.size * 0.75
        ]
        if candidates:
            largest = max(candidates, key=lambda index: stats[index, cv2.CC_STAT_AREA])
            binary = cv2.compare(labels, largest, cv2.CMP_EQ)
        else:
            binary[:] = 0

        feathered = cv2.GaussianBlur(binary, (5, 5), 0)
        if frame.shape[:2] != feathered.shape[:2]:
            feathered = cv2.resize(
                feathered,
                (frame.shape[1], frame.shape[0]),
                interpolation=cv2.INTER_LINEAR,
            )
        return feathered
