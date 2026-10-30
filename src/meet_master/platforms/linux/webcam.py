"""Linux webcam capture and local preview.

This first platform adapter acquires frames through OpenCV's Video4Linux2
backend and displays them in a local desktop window. It does not publish a
virtual camera or save frames to disk.
"""

from __future__ import annotations

from meet_master.core.gesture_recognizer import GestureObservation, GestureRecognizer


def preview(
    camera_index: int = 0,
    width: int = 1280,
    height: int = 720,
    mirror: bool = True,
    recognize_gestures: bool = False,
    model_path: str | None = None,
    gesture_threshold: float = 0.50,
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

    recognizer = (
        GestureRecognizer(model_path=model_path, confidence_threshold=gesture_threshold)
        if recognize_gestures
        else None
    )

    # CAP_V4L2 selects Linux's native webcam backend. The requested dimensions
    # are hints: hardware and driver support determine the actual frame size.
    capture = cv2.VideoCapture(camera_index, cv2.CAP_V4L2)
    if not capture.isOpened():
        capture.release()
        if recognizer is not None:
            recognizer.close()
        raise RuntimeError(
            f"impossible d’ouvrir la caméra {camera_index}. Vérifiez qu’elle existe, "
            "qu’aucune autre application ne l’utilise et que votre compte a accès à /dev/video*. "
            "Essayez un autre index avec --camera."
        )

    capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    window_name = "Meet Master — aperçu webcam"

    try:
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
                _draw_gesture_status(cv2, frame, observation)
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
            if recognizer is not None:
                recognizer.close()

    return 0


def _draw_gesture_status(cv2, frame, observation: GestureObservation) -> None:
    """Draw a short, ASCII-only status line using OpenCV's built-in font."""
    labels = {
        "Closed_Fist": "Poing ferme",
        "Open_Palm": "Paume ouverte",
        "Pointing_Up": "Index leve",
        "Thumb_Down": "Pouce baisse",
        "Thumb_Up": "Pouce leve",
        "Victory": "V de victoire",
        "ILoveYou": "Signe I love you",
    }
    if not observation.hands:
        lines = [("Aucune main detectee", (180, 180, 180))]
    else:
        side_labels = {"Left": "gauche", "Right": "droite", "Unknown": "inconnue"}
        lines = []
        for hand in observation.hands:
            side = side_labels.get(hand.handedness, hand.handedness)
            if hand.gesture:
                label = labels.get(hand.gesture, hand.gesture)
                text = f"Main {side} : {label} ({hand.confidence:.0%})"
                color = (40, 220, 100)
            elif hand.candidate in ("None", None):
                text = f"Main {side} : geste hors model ({hand.confidence:.0%})"
                color = (40, 190, 240)
            else:
                candidate = labels.get(hand.candidate, hand.candidate) if hand.candidate else "?"
                text = f"Main {side} : score faible - {candidate} ({hand.confidence:.0%})"
                color = (40, 190, 240)
            lines.append((text, color))

    for line_index, (text, color) in enumerate(lines):
        cv2.putText(
            frame,
            text,
            (16, 64 + line_index * 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            color,
            2,
            cv2.LINE_AA,
        )
