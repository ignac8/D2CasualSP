import shutil
from pathlib import Path

from casc_extract import extract_d2r_files
from diablo_reader import DiabloReader
from platform_utils import get_d2r_path

SCRIPT_DIR = Path(__file__).parent
TEMPLATES_DIR = SCRIPT_DIR / "templates/D2RCasualSP/D2RCasualSP.mpq/data/global/excel"
WORK_DIR = SCRIPT_DIR / "work"
EXTRACTED_DIR = WORK_DIR / "data/data/global/excel"
D2R_PATH = get_d2r_path()


def read_file(path):
    with open(path, "r", encoding="utf-8-sig") as f:
        return list(DiabloReader(f))


def compare_files(template_path, extracted_path):
    t_rows = read_file(template_path)
    e_rows = read_file(extracted_path)
    diffs = []

    t_keys = list(t_rows[0].keys()) if t_rows else []
    e_keys = list(e_rows[0].keys()) if e_rows else []
    added_cols = set(e_keys) - set(t_keys)
    removed_cols = set(t_keys) - set(e_keys)
    if added_cols:
        diffs.append(f"  New columns: {', '.join(sorted(added_cols))}")
    if removed_cols:
        diffs.append(f"  Removed columns: {', '.join(sorted(removed_cols))}")

    min_rows = min(len(t_rows), len(e_rows))
    for i in range(min_rows):
        all_keys = set(list(t_rows[i].keys()) + list(e_rows[i].keys()))
        for key in sorted(all_keys):
            tv = t_rows[i].get(key, "")
            ev = e_rows[i].get(key, "")
            if tv != ev:
                row_id = t_rows[i].get("index", t_rows[i].get("skilldesc",
                         t_rows[i].get("name", t_rows[i].get("*ID", f"row {i}"))))
                diffs.append(f'  Row {i} [{row_id}] "{key}": "{tv}" -> "{ev}"')

    if len(t_rows) != len(e_rows):
        diffs.append(f"  Row count: {len(t_rows)} -> {len(e_rows)}")

    return diffs


def main():
    print("=" * 60)
    print("Step 1: Extracting files from D2R CASC storage")
    print("=" * 60)
    extract_d2r_files(D2R_PATH, WORK_DIR)
    print()

    print("=" * 60)
    print("Step 2: Comparing extracted files with templates")
    print("=" * 60)

    template_files = {f.name for f in TEMPLATES_DIR.glob("*.txt")}
    extracted_files = {f.name for f in EXTRACTED_DIR.glob("*.txt")}

    new_files = sorted(extracted_files - template_files)
    removed_files = sorted(template_files - extracted_files)
    common_files = sorted(template_files & extracted_files)

    if new_files:
        print(f"\nNew files ({len(new_files)}):")
        for f in new_files:
            print(f"  + {f}")

    if removed_files:
        print(f"\nRemoved files ({len(removed_files)}):")
        for f in removed_files:
            print(f"  - {f}")

    changed_files = []
    for fname in common_files:
        diffs = compare_files(TEMPLATES_DIR / fname, EXTRACTED_DIR / fname)
        if diffs:
            changed_files.append((fname, diffs))

    if changed_files:
        print(f"\nChanged files ({len(changed_files)}):")
        for fname, diffs in changed_files:
            print(f"\n  {fname}:")
            for d in diffs:
                print(f"  {d}")
    print()

    total_changes = len(new_files) + len(removed_files) + len(changed_files)
    if total_changes == 0:
        print("Templates are up to date. No changes needed.")
        return

    print(f"Summary: {len(new_files)} new, {len(removed_files)} removed, {len(changed_files)} changed")

    print()
    print("=" * 60)
    print("Step 3: Updating templates")
    print("=" * 60)

    for fname in new_files:
        shutil.copy2(EXTRACTED_DIR / fname, TEMPLATES_DIR / fname)
        print(f"  Added {fname}")

    for fname in removed_files:
        (TEMPLATES_DIR / fname).unlink()
        print(f"  Removed {fname}")

    for fname, _ in changed_files:
        shutil.copy2(EXTRACTED_DIR / fname, TEMPLATES_DIR / fname)
        print(f"  Updated {fname}")

    print(f"\nDone. Run python3 build_and_deploy.py to regenerate and deploy.")


if __name__ == "__main__":
    main()
