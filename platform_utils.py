import sys
from enum import Enum
from pathlib import Path


class Platform(Enum):
    WINDOWS = "windows"
    WSL = "wsl"
    LINUX = "linux"


def detect_platform():
    if sys.platform == "win32":
        return Platform.WINDOWS
    try:
        if "microsoft" in Path("/proc/version").read_text().lower():
            return Platform.WSL
    except OSError:
        pass
    return Platform.LINUX


D2R_BASE = {
    Platform.WINDOWS: Path(r"C:\Program Files (x86)\Diablo II Resurrected"),
    Platform.WSL: Path("/mnt/c/Program Files (x86)/Diablo II Resurrected"),
    Platform.LINUX: Path.home() / "Games/bnet/pfx/drive_c/Program Files (x86)/Diablo II Resurrected",
}


def get_d2r_path():
    return D2R_BASE[detect_platform()]


def get_d2r_mods_path():
    return get_d2r_path() / "mods"
