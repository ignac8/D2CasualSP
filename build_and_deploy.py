import shutil
import subprocess
import sys
from pathlib import Path

from platform_utils import get_d2r_mods_path

SCRIPT_DIR = Path(__file__).parent
MOD_NAME = "D2RCasualSP"


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
    mods_path = get_d2r_mods_path()
    generate()
    deploy(mods_path)


if __name__ == "__main__":
    main()
