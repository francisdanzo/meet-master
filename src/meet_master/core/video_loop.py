"""Local video playback that restarts cleanly at end of file."""

from __future__ import annotations

from pathlib import Path
import time


class VideoLoop:
    """Decode a local clip at its reported frame rate and loop it indefinitely."""

    def __init__(self, path: str | Path):
        try:
            import cv2
        except ImportError as error:
            raise RuntimeError("OpenCV est nécessaire pour lire la vidéo de remplacement") from error

        self._cv2 = cv2
        self.path = Path(path).expanduser()
        if not self.path.is_file():
            raise RuntimeError(f"vidéo de remplacement introuvable : {self.path}")

        self._capture = cv2.VideoCapture(str(self.path))
        if not self._capture.isOpened():
            self._capture.release()
            raise RuntimeError(
                f"OpenCV ne peut pas lire cette vidéo : {self.path}. "
                "Vérifiez le format et le codec du fichier."
            )

        fps = float(self._capture.get(cv2.CAP_PROP_FPS))
        self._frame_interval = 1.0 / fps if 1.0 <= fps <= 120.0 else 1.0 / 25.0
        self._next_frame_at = 0.0
        self._frame = None
        self._rendered_frame = None
        self.restart()

    def restart(self) -> None:
        """Start this absence session from the clip's first frame."""
        self._capture.set(self._cv2.CAP_PROP_POS_FRAMES, 0)
        self._next_frame_at = time.monotonic()
        self._frame = None
        self._rendered_frame = None

    def read(self, width: int, height: int):
        """Return the next presentation-time frame fitted inside the target size."""
        if width <= 0 or height <= 0:
            raise ValueError("la taille de sortie vidéo doit être positive")

        now = time.monotonic()
        frames_read = 0
        while self._frame is None or now >= self._next_frame_at:
            self._read_next_frame()
            self._next_frame_at += self._frame_interval
            frames_read += 1
            if frames_read >= 240:
                # Avoid an unbounded catch-up loop after a long application pause.
                self._next_frame_at = now + self._frame_interval
                break

        if self._rendered_frame is None:
            self._rendered_frame = self._fit_frame(self._frame, width, height)
        return self._rendered_frame

    def _read_next_frame(self) -> None:
        ok, frame = self._capture.read()
        if not ok or frame is None:
            self._capture.set(self._cv2.CAP_PROP_POS_FRAMES, 0)
            ok, frame = self._capture.read()
        if not ok or frame is None:
            raise RuntimeError(f"impossible de décoder des images dans {self.path}")
        self._frame = frame
        self._rendered_frame = None

    def _fit_frame(self, frame, width: int, height: int):
        """Resize without cropping and center the clip on a dark letterbox."""
        source_height, source_width = frame.shape[:2]
        scale = min(width / source_width, height / source_height)
        fitted_width = max(1, round(source_width * scale))
        fitted_height = max(1, round(source_height * scale))
        resized = self._cv2.resize(frame, (fitted_width, fitted_height))
        horizontal = width - fitted_width
        vertical = height - fitted_height
        left = horizontal // 2
        right = horizontal - left
        top = vertical // 2
        bottom = vertical - top
        return self._cv2.copyMakeBorder(
            resized,
            top,
            bottom,
            left,
            right,
            self._cv2.BORDER_CONSTANT,
            value=(20, 16, 32),
        )

    def close(self) -> None:
        """Release the video decoder."""
        self._capture.release()
