"""Publish composed frames through a Linux v4l2loopback camera."""

from __future__ import annotations


class LinuxVirtualCamera:
    """Send BGR frames to an existing v4l2loopback device."""

    def __init__(self, width: int, height: int, fps: float = 30.0, device: str | None = None):
        try:
            import pyvirtualcam
        except ImportError as error:
            raise RuntimeError(
                "pyvirtualcam est absent. Installez l’extra avec « python -m pip install -e '.[virtual-camera]' »."
            ) from error

        try:
            self._camera = pyvirtualcam.Camera(
                width=width,
                height=height,
                fps=fps,
                fmt=pyvirtualcam.PixelFormat.BGR,
                device=device,
                backend="v4l2loopback",
            )
        except Exception as error:
            device_hint = f" ({device})" if device else ""
            raise RuntimeError(
                f"impossible d’ouvrir la caméra virtuelle{device_hint}. "
                "Installez le module v4l2loopback correspondant à votre noyau, "
                "puis chargez-le avec « sudo modprobe v4l2loopback devices=1 exclusive_caps=1 card_label='Meet Master' ». "
                f"Détail : {error}"
            ) from error

        self.device = self._camera.device

    def send(self, frame) -> None:
        """Publish one BGR frame and pace output to the selected camera FPS."""
        import numpy as np

        try:
            self._camera.send(np.ascontiguousarray(frame))
            self._camera.sleep_until_next_frame()
        except Exception as error:
            raise RuntimeError(f"échec d’envoi vers {self.device} : {error}") from error

    def close(self) -> None:
        """Release the virtual camera device."""
        self._camera.close()
