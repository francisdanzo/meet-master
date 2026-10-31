"""Application cache locations and per-run temporary storage."""

from __future__ import annotations

import os
from pathlib import Path
import sys
from tempfile import TemporaryDirectory


def app_cache_directory() -> Path:
    """Return Meet Master's user cache directory for the current platform."""
    if sys.platform == "win32":
        base = os.environ.get("LOCALAPPDATA")
        if base:
            return Path(base) / "MeetMaster" / "Cache"
        return Path.home() / "AppData" / "Local" / "MeetMaster" / "Cache"

    if sys.platform == "darwin":
        return Path.home() / "Library" / "Caches" / "MeetMaster"

    base = os.environ.get("XDG_CACHE_HOME")
    return (Path(base) if base else Path.home() / ".cache") / "meet-master"


def create_session_cache() -> TemporaryDirectory[str]:
    """Create a unique session folder under the app cache; caller cleans it."""
    cache_dir = app_cache_directory()
    try:
        cache_dir.mkdir(parents=True, exist_ok=True)
        return TemporaryDirectory(prefix="session-", dir=cache_dir)
    except OSError as error:
        raise RuntimeError(
            f"impossible de créer le cache Meet Master dans {cache_dir} : {error}"
        ) from error
