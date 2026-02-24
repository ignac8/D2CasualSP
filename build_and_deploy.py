import shutil
import subprocess
import sys
from enum import Enum
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
MOD_NAME = "D2RCasualSP"


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


D2R_MODS = {
    Platform.WINDOWS: Path(r"C:\Program Files (x86)\Diablo II Resurrected\mods"),
    Platform.WSL: Path("/mnt/c/Program Files (x86)/Diablo II Resurrected/mods"),
    Platform.LINUX: Path.home() / "Games/bnet/pfx/drive_c/Program Files (x86)/Diablo II Resurrected/mods",
}


def generate():
    print("[1/2] Generating mod files...")
    subprocess.run([sys.executable, str(SCRIPT_DIR / "main.py")], cwd=SCRIPT_DIR, check=True)
    print("  Done")


def deploy(mods_path):
    print(f"[2/2] Deploying to {mods_path}...")
    dest = mods_path / MOD_NAME
    if dest.exists():
        if not (dest / f"{MOD_NAME}.mpq").exists():
            sys.exit(f"Error: {dest} exists but doesn't contain {MOD_NAME}.mpq — refusing to delete")
        shutil.rmtree(dest)
    mods_path.mkdir(parents=True, exist_ok=True)
    shutil.copytree(SCRIPT_DIR / "results" / MOD_NAME, dest)
    print("  Done")


def main():
    mods_path = D2R_MODS[detect_platform()]
    generate()
    deploy(mods_path)


if __name__ == "__main__":
    main()
