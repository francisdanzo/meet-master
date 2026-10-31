"""Linux webcam capture and local preview.

Gesture mode records a temporary background clip unless the user supplies a
replacement clip explicitly.
"""

from __future__ import annotations

from meet_master.core.cache import create_session_cache
from meet_master.core.gesture_recognizer import GestureObservation, GestureRecognizer
from meet_master.core.presence import PresenceController, PresenceState
from meet_master.core.video_loop import VideoLoop
from meet_master.platforms.linux.background_capture import record_absence_background


def preview(
    camera_index: int = 0,
    width: int = 1280,
    height: int = 720,
    mirror: bool = True,
    recognize_gestures: bool = False,
    model_path: str | None = None,
    gesture_threshold: float = 0.50,
    away_video_path: str | None = None,
) -> int:
    """Show a webcam preview until the user presses q or Escape.

    Args:
        camera_index: OpenCV/V4L2 camera index to open.
        width: Requested capture width in pixels; the camera may choose another.
        height: Requested capture height in pixels; the camera may choose another.
        mirror: Flip each displayed frame horizontally, like a mirror.
        recognize_gestures: Run the shared gesture model and show its result.
        model_path: Optional local MediaPipe model file; otherwise use the cache.
        gesture_threshold: Minimum classifier score to mark a gesture as recognized.
        away_video_path: Optional local clip; otherwise gesture mode records
            a temporary background clip at startup.

    Returns:
        Zero after a normal user exit.

    Raises:
        RuntimeError: If OpenCV is unavailable or the camera cannot be opened.
    """
    try:
        import cv2
    except ImportError as error:
        raise RuntimeError(
            "OpenCV est absent. Activez l’environnement virtuel puis lancez « python -m pip install -e . »."
        ) from error

    if camera_index < 0:
        raise RuntimeError("l’index de caméra doit être positif ou nul")
    if width <= 0 or height <= 0:
        raise RuntimeError("la largeur et la hauteur doivent être supérieures à zéro")

    replacement_video = VideoLoop(away_video_path) if away_video_path else None
    try:
        recognizer = (
            GestureRecognizer(model_path=model_path, confidence_threshold=gesture_threshold)
            if recognize_gestures
            else None
        )
    except Exception:
        if replacement_video is not None:
            replacement_video.close()
        raise
    presence = PresenceController() if recognize_gestures else None

    # CAP_V4L2 selects Linux's native webcam backend. The requested dimensions
    # are hints: hardware and driver support determine the actual frame size.
    capture = cv2.VideoCapture(camera_index, cv2.CAP_V4L2)
    if not capture.isOpened():
        capture.release()
        if recognizer is not None:
            recognizer.close()
        if replacement_video is not None:
            replacement_video.close()
        raise RuntimeError(
            f"impossible d’ouvrir la caméra {camera_index}. Vérifiez qu’elle existe, "
            "qu’aucune autre application ne l’utilise et que votre compte a accès à /dev/video*. "
            "Essayez un autre index avec --camera."
        )

    capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    window_name = "Meet Master — aperçu webcam"
    temporary_video_dir = None

    try:
        if recognize_gestures and replacement_video is None:
            temporary_video_dir = create_session_cache()
            background_path = f"{temporary_video_dir.name}/arriere-plan.avi"
            print("Préparation de la vidéo d’absence : sors du champ pendant 5 secondes.")
            frame_count = record_absence_background(
                capture,
                cv2,
                background_path,
                window_name,
                mirror=mirror,
            )
            replacement_video = VideoLoop(background_path)
            print(
                f"Fond enregistré ({frame_count} images). "
                f"Clip en cache : {background_path} (supprimé à la fermeture)."
            )

        while True:
            ok, frame = capture.read()
            if not ok or frame is None:
                raise RuntimeError("la caméra est ouverte, mais aucune image n’a pu être lue")

            if mirror:
                frame = cv2.flip(frame, 1)

            observation = (
                recognizer.recognize(frame, mirrored_input=mirror)
                if recognizer is not None
                else None
            )
            if presence is not None and observation is not None:
                new_state = presence.update(observation)
                if new_state is PresenceState.AWAY and replacement_video is not None:
                    replacement_video.restart()

            if presence is not None and presence.state is PresenceState.AWAY:
                if replacement_video is not None:
                    frame = replacement_video.read(frame.shape[1], frame.shape[0])
                    cv2.putText(
                        frame,
                        "ABSENCE ACTIVE | Montre V pour revenir",
                        (16, 32),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.65,
                        (255, 255, 255),
                        2,
                        cv2.LINE_AA,
                    )
                else:
                    frame = frame.copy()
                    frame[:] = (20, 16, 32)
                    cv2.putText(
                        frame,
                        "ABSENCE ACTIVE",
                        (24, 64),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.0,
                        (255, 255, 255),
                        2,
                        cv2.LINE_AA,
                    )
                    cv2.putText(
                        frame,
                        "Montre le signe V pour revenir",
                        (24, 104),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (190, 200, 230),
                        2,
                        cv2.LINE_AA,
                    )
                    cv2.putText(
                        frame,
                        "Ecran provisoire - video de remplacement a venir",
                        (24, 140),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.55,
                        (150, 160, 190),
                        1,
                        cv2.LINE_AA,
                    )
            elif presence is not None:
                cv2.putText(
                    frame,
                    "PRESENT | Montre le signe V pour partir",
                    (16, 32),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.65,
                    (40, 220, 100),
                    2,
                    cv2.LINE_AA,
                )
            else:
                cv2.putText(
                    frame,
                    "Meet Master | q ou Echap pour quitter",
                    (16, 32),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.65,
                    (40, 220, 100),
                    2,
                    cv2.LINE_AA,
                )
            if observation is not None:
                status_y = 184 if (presence is not None and presence.state is PresenceState.AWAY and replacement_video is None) else 64
                _draw_gesture_status(cv2, frame, observation, status_y)
            cv2.imshow(window_name, frame)
            key = cv2.waitKey(1) & 0xFF
            if key in (ord("q"), 27):
                break
    except cv2.error as error:
        raise RuntimeError(
            "OpenCV n’a pas pu afficher la fenêtre. Vérifiez que vous êtes dans une session graphique."
        ) from error
    finally:
        capture.release()
        try:
            cv2.destroyAllWindows()
        finally:
            try:
                if recognizer is not None:
                    recognizer.close()
            finally:
                try:
                    if replacement_video is not None:
                        replacement_video.close()
                finally:
                    if temporary_video_dir is not None:
                        temporary_video_dir.cleanup()

    return 0


def _draw_gesture_status(cv2, frame, observation: GestureObservation, top: int = 64) -> None:
    """Draw a short, ASCII-only status line using OpenCV's built-in font."""
    labels = {
        "Closed_Fist": "Poing ferme",
        "Open_Palm": "Paume ouverte",
        "Pointing_Up": "Index leve",
        "Thumb_Down": "Pouce baisse",
        "Thumb_Up": "Pouce leve",
        "Victory": "V de victoire",
        "ILoveYou": "Signe I love you",
        "Horns": "Cornes rock",
        "CrossedFingers": "Doigts croises",
        "MiddleFinger": "Majeur leve",
        "OK": "Signe OK",
        "PinchedFingers": "Doigts pinces",
        "Pinch": "Pincement pouce-index",
        "VulcanSalute": "Salut vulcain",
        "PointingRight": "Index vers droite",
        "PointingLeft": "Index vers gauche",
        "PointingDown": "Index vers bas",
        "PointingAtViewer": "Index vers camera",
    }
    if not observation.hands:
        lines = [("Aucune main detectee", (180, 180, 180))]
    else:
        side_labels = {"Left": "gauche", "Right": "droite", "Unknown": "inconnue"}
        lines = []
        for hand in observation.hands:
            side = side_labels.get(hand.handedness, hand.handedness)
            candidate_text = " | ".join(
                f"{labels.get(name, 'Autre' if name == 'None' else name)} {score:.0%}"
                for name, score in hand.ranked_candidates[:3]
            )
            if not candidate_text:
                candidate_text = "aucun candidat"

            if hand.rule_based and hand.candidate == "AmbiguousVictoryPointing":
                text = f"Main {side} : ambigu - V ou index; tends mieux le majeur"
                color = (40, 190, 240)
            elif hand.rule_based:
                label = labels.get(hand.gesture, hand.gesture)
                rotation_note = (
                    ", rotation libre"
                    if hand.gesture in {"Victory", "ILoveYou", "Horns"}
                    else ""
                )
                text = f"Main {side} : {label} (forme{rotation_note})"
                color = (40, 220, 100)
            elif hand.gesture:
                text = f"Main {side} : {candidate_text}"
                color = (40, 220, 100)
            elif hand.candidate in ("None", None):
                text = f"Main {side} : hors gestes appris | {candidate_text}"
                color = (40, 190, 240)
            else:
                text = f"Main {side} : score faible | {candidate_text}"
                color = (40, 190, 240)
            lines.append((text, color))

    for line_index, (text, color) in enumerate(lines):
        cv2.putText(
            frame,
            text,
            (16, top + line_index * 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            color,
            2,
            cv2.LINE_AA,
        )
