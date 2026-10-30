"""Shared MediaPipe gesture recognition, independent of webcam hardware."""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import shutil
import time
from urllib.error import URLError
from urllib.request import urlopen


MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/gesture_recognizer/"
    "gesture_recognizer/float16/1/gesture_recognizer.task"
)


@dataclass(frozen=True)
class HandGestureObservation:
    """Recognized side and gesture for one hand in a frame."""

    handedness: str
    gesture: str | None
    confidence: float
    candidate: str | None = None


@dataclass(frozen=True)
class GestureObservation:
    """All hands recognized in one frame, in MediaPipe's detection order."""

    hands: tuple[HandGestureObservation, ...]


def _default_model_path() -> Path:
    """Return the per-user cache path for the official model asset."""
    cache_root = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache"))
    return cache_root / "meet-master" / "gesture_recognizer.task"


def _ensure_model(model_path: str | Path | None) -> Path:
    """Use a caller-provided model or fetch the official model once to cache."""
    if model_path is not None:
        path = Path(model_path).expanduser()
        if not path.is_file():
            raise RuntimeError(f"modèle MediaPipe introuvable : {path}")
        return path

    path = _default_model_path()
    if path.is_file() and path.stat().st_size > 0:
        return path

    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_suffix(".task.part")
    try:
        with urlopen(MODEL_URL, timeout=30) as response, temporary_path.open("wb") as output:
            shutil.copyfileobj(response, output)
        if temporary_path.stat().st_size == 0:
            raise RuntimeError("le téléchargement du modèle a produit un fichier vide")
        temporary_path.replace(path)
    except (OSError, URLError, TimeoutError, RuntimeError) as error:
        temporary_path.unlink(missing_ok=True)
        raise RuntimeError(
            "impossible de télécharger le modèle de gestes. Vérifiez votre connexion, "
            "ou téléchargez le modèle officiel et relancez avec --model CHEMIN."
        ) from error

    return path


class GestureRecognizer:
    """Run MediaPipe's pretrained gesture model on video frames.

    The class accepts OpenCV BGR frames, converts them to RGB, and uses
    MediaPipe's video mode with strictly increasing monotonic timestamps.
    Camera acquisition and user-interface drawing remain outside this class.
    """

    def __init__(self, model_path: str | Path | None = None, confidence_threshold: float = 0.50):
        if not 0.0 <= confidence_threshold <= 1.0:
            raise ValueError("le seuil de confiance doit être compris entre 0 et 1")

        try:
            import mediapipe as mp
            from mediapipe.tasks import python as mp_python
            from mediapipe.tasks.python import vision
        except ImportError as error:
            raise RuntimeError(
                "MediaPipe est absent. Installez l’option gestes avec « python -m pip install -e '.[gestures]' »."
            ) from error

        self._cv2 = self._load_opencv()
        self._mp = mp
        self._confidence_threshold = confidence_threshold
        self._last_timestamp_ms = -1

        try:
            resolved_model = _ensure_model(model_path)
            options = vision.GestureRecognizerOptions(
                base_options=mp_python.BaseOptions(model_asset_path=str(resolved_model)),
                running_mode=vision.RunningMode.VIDEO,
                num_hands=2,
                min_hand_detection_confidence=0.5,
                min_hand_presence_confidence=0.5,
                min_tracking_confidence=0.5,
            )
            self._recognizer = vision.GestureRecognizer.create_from_options(options)
            self._image_format = mp.ImageFormat.SRGB
        except (OSError, ValueError, RuntimeError) as error:
            raise RuntimeError(f"impossible de préparer la reconnaissance gestuelle : {error}") from error

    @staticmethod
    def _load_opencv():
        """Import OpenCV lazily so core modules remain easy to import."""
        try:
            import cv2
        except ImportError as error:
            raise RuntimeError("OpenCV est nécessaire pour analyser les images de la webcam") from error
        return cv2

    def recognize(self, frame_bgr, mirrored_input: bool = False) -> GestureObservation:
        """Classify up to two hands in a BGR image.

        MediaPipe's handedness output flips when the input frame is mirrored.
        Set ``mirrored_input`` when the preview has been horizontally flipped
        so the returned side still refers to the user's actual left or right hand.
        """
        rgb_frame = self._cv2.cvtColor(frame_bgr, self._cv2.COLOR_BGR2RGB)
        image = self._mp.Image(image_format=self._image_format, data=rgb_frame)
        timestamp_ms = max(time.monotonic_ns() // 1_000_000, self._last_timestamp_ms + 1)
        self._last_timestamp_ms = timestamp_ms
        result = self._recognizer.recognize_for_video(image, timestamp_ms)

        hands: list[HandGestureObservation] = []
        for index, _landmarks in enumerate(result.hand_landmarks):
            handedness = "Unknown"
            if index < len(result.handedness) and result.handedness[index]:
                handedness = result.handedness[index][0].category_name or "Unknown"
            if mirrored_input:
                handedness = {"Left": "Right", "Right": "Left"}.get(handedness, handedness)

            candidate = None
            confidence = 0.0
            if index < len(result.gestures) and result.gestures[index]:
                category = result.gestures[index][0]
                candidate = category.category_name
                confidence = float(category.score or 0.0)

            gesture = candidate
            if candidate in (None, "None") or confidence < self._confidence_threshold:
                gesture = None

            hands.append(HandGestureObservation(handedness, gesture, confidence, candidate))

        return GestureObservation(tuple(hands))

    def close(self) -> None:
        """Release MediaPipe's native recognizer resources."""
        self._recognizer.close()

    def __enter__(self) -> "GestureRecognizer":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()
