"""Record a short, temporary empty-room plate from the webcam."""

from __future__ import annotations

import math
from pathlib import Path
import time

import numpy as np


def record_absence_background(
    capture,
    cv2,
    output_path: str | Path,
    window_name: str,
    mirror: bool = True,
    leave_seconds: float = 5.0,
    record_seconds: float = 3.0,
) -> tuple[int, object]:
    """Prompt the user to leave frame, then record a short background clip.

    The file is encoded as a small, silent MJPEG AVI. The caller owns its
    temporary directory and is responsible for deleting it when the preview
    session ends.
    """
    if leave_seconds < 0 or record_seconds <= 0:
        raise ValueError("le délai doit être positif et la durée d’enregistrement doit être supérieure à zéro")

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    countdown_end = time.monotonic() + leave_seconds

    while time.monotonic() < countdown_end:
        frame = _read_frame(capture)
        shown = cv2.flip(frame, 1) if mirror else frame.copy()
        remaining = max(0, math.ceil(countdown_end - time.monotonic()))
        cv2.putText(
            shown,
            f"Sors du champ - capture dans {remaining}s",
            (16, 42),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (40, 220, 255),
            2,
            cv2.LINE_AA,
        )
        cv2.putText(
            shown,
            "Echap pour annuler",
            (16, 74),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (230, 230, 230),
            1,
            cv2.LINE_AA,
        )
        cv2.imshow(window_name, shown)
        if cv2.waitKey(1) & 0xFF == 27:
            raise RuntimeError("enregistrement du fond annulé par l’utilisateur")

    frame = _read_frame(capture)
    source_height, source_width = frame.shape[:2]
    scale = min(1.0, 640 / source_width, 360 / source_height)
    output_width = max(1, round(source_width * scale))
    output_height = max(1, round(source_height * scale))
    writer = cv2.VideoWriter(
        str(output_path),
        cv2.VideoWriter_fourcc(*"MJPG"),
        15.0,
        (output_width, output_height),
    )
    if not writer.isOpened():
        writer.release()
        raise RuntimeError(
            "OpenCV ne peut pas créer le fichier temporaire MJPEG. "
            "Vérifiez que le codec MJPEG est disponible dans cette installation."
        )

    started_at = time.monotonic()
    deadline = started_at + record_seconds
    next_frame_at = started_at
    frame_interval = 1.0 / 15.0
    frame_count = 0
    background_sum = None
    try:
        while time.monotonic() < deadline:
            frame = _read_frame(capture)
            now = time.monotonic()
            recorded_frame = cv2.flip(frame, 1) if mirror else frame
            recorded_frame = cv2.resize(recorded_frame, (output_width, output_height))
            if now >= next_frame_at:
                writer.write(recorded_frame)
                if background_sum is None:
                    background_sum = np.zeros(
                        (output_height, output_width, 3), dtype=np.float32
                    )
                cv2.accumulate(recorded_frame, background_sum)
                frame_count += 1
                next_frame_at += frame_interval
                if next_frame_at < now:
                    next_frame_at = now + frame_interval

            shown = recorded_frame.copy()
            seconds_left = max(0.0, deadline - time.monotonic())
            cv2.putText(
                shown,
                f"Enregistrement du fond - {seconds_left:.1f}s",
                (12, 28),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (40, 220, 255),
                2,
                cv2.LINE_AA,
            )
            cv2.imshow(window_name, shown)
            if cv2.waitKey(1) & 0xFF == 27:
                raise RuntimeError("enregistrement du fond annulé par l’utilisateur")
    finally:
        writer.release()

    if frame_count == 0 or not output_path.is_file() or output_path.stat().st_size == 0:
        raise RuntimeError("la capture du fond n’a enregistré aucune image")
    reference = cv2.convertScaleAbs(background_sum, alpha=1.0 / frame_count)
    return frame_count, reference


def _read_frame(capture):
    """Read one camera frame or report a clear calibration error."""
    ok, frame = capture.read()
    if not ok or frame is None:
        raise RuntimeError("la webcam n’a pas fourni d’image pendant l’enregistrement du fond")
    return frame
