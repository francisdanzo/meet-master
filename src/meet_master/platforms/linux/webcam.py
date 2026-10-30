"""Linux webcam capture and local preview.

This first platform adapter acquires frames through OpenCV's Video4Linux2
backend and displays them in a local desktop window. It does not publish a
virtual camera or save frames to disk.
"""

from __future__ import annotations


def preview(camera_index: int = 0, width: int = 1280, height: int = 720, mirror: bool = True) -> int:
    """Show a webcam preview until the user presses q or Escape.

    Args:
        camera_index: OpenCV/V4L2 camera index to open.
        width: Requested capture width in pixels; the camera may choose another.
        height: Requested capture height in pixels; the camera may choose another.
        mirror: Flip each displayed frame horizontally, like a mirror.

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

    # CAP_V4L2 selects Linux's native webcam backend. The requested dimensions
    # are hints: hardware and driver support determine the actual frame size.
    capture = cv2.VideoCapture(camera_index, cv2.CAP_V4L2)
    if not capture.isOpened():
        capture.release()
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

            cv2.putText(
                frame,
                "Apercu Meet Master | q ou Echap pour quitter",
                (16, 32),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                (40, 220, 100),
                2,
                cv2.LINE_AA,
            )
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
        cv2.destroyAllWindows()

    return 0
