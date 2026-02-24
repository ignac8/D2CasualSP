import io
import sys
from pathlib import Path

from diablo_reader import DiabloReader
from diablo_writer import DiabloWriter

SCRIPT_DIR = Path(__file__).parent
TEMPLATES_DIR = SCRIPT_DIR / "templates/D2RCasualSP/D2RCasualSP.mpq/data/global/excel"


def test_file(path):
    with open(path, mode='r', newline='') as f:
        original = f.read()

    with open(path, mode='r', newline='') as f:
        reader = DiabloReader(f)
        output = io.StringIO()
        writer = DiabloWriter(output, fieldnames=reader.fieldnames)
        writer.write_header()
        for row in reader:
            writer.write_row(row)

    return original == output.getvalue()


def main():
    files = sorted(TEMPLATES_DIR.glob("*.txt"))
    failed = []

    for path in files:
        if test_file(path):
            print(f"  PASS  {path.name}")
        else:
            print(f"  FAIL  {path.name}")
            failed.append(path.name)

    print()
    if failed:
        print(f"{len(failed)}/{len(files)} files failed: {', '.join(failed)}")
        sys.exit(1)
    else:
        print(f"All {len(files)} files passed")


if __name__ == "__main__":
    main()
