import ctypes
import ctypes.util
import os
import sys
from pathlib import Path

MAX_PATH = 1024
MD5_HASH_SIZE = 16
CASC_LOCALE_ALL = 0xFFFFFFFF
CASC_OPEN_BY_NAME = 0x00000000

class CASC_FIND_DATA(ctypes.Structure):
    _fields_ = [
        ("szFileName", ctypes.c_char * MAX_PATH),
        ("CKey", ctypes.c_ubyte * MD5_HASH_SIZE),
        ("EKey", ctypes.c_ubyte * MD5_HASH_SIZE),
        ("TagBitMask", ctypes.c_uint64),
        ("FileSize", ctypes.c_uint64),
        ("szPlainName", ctypes.c_char_p),
        ("dwFileDataId", ctypes.c_uint32),
        ("dwLocaleFlags", ctypes.c_uint32),
        ("dwContentFlags", ctypes.c_uint32),
        ("dwSpanCount", ctypes.c_uint32),
        ("bFileAvailable", ctypes.c_uint32),
        ("NameType", ctypes.c_int),
    ]

SCRIPT_DIR = Path(__file__).parent
CASCLIB_PATH = SCRIPT_DIR / "CascLib" / "build" / "libcasc.so"

if not CASCLIB_PATH.exists():
    print(f"Error: CascLib not found at {CASCLIB_PATH}")
    print("Build it first: cd CascLib/build && cmake .. && make")
    sys.exit(1)

casc = ctypes.CDLL(str(CASCLIB_PATH))

casc.CascOpenStorage.argtypes = [ctypes.c_char_p, ctypes.c_uint32, ctypes.POINTER(ctypes.c_void_p)]
casc.CascOpenStorage.restype = ctypes.c_bool

casc.CascCloseStorage.argtypes = [ctypes.c_void_p]
casc.CascCloseStorage.restype = ctypes.c_bool

casc.CascFindFirstFile.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.POINTER(CASC_FIND_DATA), ctypes.c_char_p]
casc.CascFindFirstFile.restype = ctypes.c_void_p

casc.CascFindNextFile.argtypes = [ctypes.c_void_p, ctypes.POINTER(CASC_FIND_DATA)]
casc.CascFindNextFile.restype = ctypes.c_bool

casc.CascFindClose.argtypes = [ctypes.c_void_p]
casc.CascFindClose.restype = ctypes.c_bool

casc.CascOpenFile.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_uint32, ctypes.c_uint32, ctypes.POINTER(ctypes.c_void_p)]
casc.CascOpenFile.restype = ctypes.c_bool

casc.CascGetFileSize64.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint64)]
casc.CascGetFileSize64.restype = ctypes.c_bool

casc.CascReadFile.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint32)]
casc.CascReadFile.restype = ctypes.c_bool

casc.CascCloseFile.argtypes = [ctypes.c_void_p]
casc.CascCloseFile.restype = ctypes.c_bool

casc.GetCascError.argtypes = []
casc.GetCascError.restype = ctypes.c_uint32

def extract_d2r_files(d2r_path: Path, output_dir: Path):
    storage_path = d2r_path / "Data"
    if not storage_path.exists():
        print(f"Error: D2R Data directory not found at {storage_path}")
        sys.exit(1)

    h_storage = ctypes.c_void_p()
    path_bytes = str(storage_path).encode("utf-8")
    if not casc.CascOpenStorage(path_bytes, CASC_LOCALE_ALL, ctypes.byref(h_storage)):
        err = casc.GetCascError()
        print(f"Error: Failed to open CASC storage at {storage_path} (error {err})")
        sys.exit(1)

    print(f"Opened CASC storage: {storage_path}")

    find_data = CASC_FIND_DATA()
    matching_files = []

    h_find = casc.CascFindFirstFile(h_storage, b"*", ctypes.byref(find_data), None)
    if not h_find or h_find == ctypes.c_void_p(-1).value:
        print("Error: CascFindFirstFile failed")
        casc.CascCloseStorage(h_storage)
        sys.exit(1)

    while True:
        filename = find_data.szFileName.decode("utf-8", errors="replace")
        normalized = filename.replace("\\", "/").lower()
        if "data/global/excel/" in normalized and normalized.endswith(".txt"):
            matching_files.append(filename)

        if not casc.CascFindNextFile(h_find, ctypes.byref(find_data)):
            break

    casc.CascFindClose(h_find)
    print(f"Found {len(matching_files)} excel .txt files")

    if not matching_files:
        print("No matching files found. Listing some files from storage to debug:")
        h_find = casc.CascFindFirstFile(h_storage, b"*", ctypes.byref(find_data), None)
        if h_find and h_find != ctypes.c_void_p(-1).value:
            count = 0
            while count < 50:
                filename = find_data.szFileName.decode("utf-8", errors="replace")
                print(f"  {filename}")
                count += 1
                if not casc.CascFindNextFile(h_find, ctypes.byref(find_data)):
                    break
            casc.CascFindClose(h_find)
        casc.CascCloseStorage(h_storage)
        sys.exit(1)

    extracted = 0
    failed = 0
    for filename in sorted(matching_files):
        h_file = ctypes.c_void_p()
        file_bytes = filename.encode("utf-8")

        if not casc.CascOpenFile(h_storage, file_bytes, 0, CASC_OPEN_BY_NAME, ctypes.byref(h_file)):
            err = casc.GetCascError()
            print(f"  SKIP {filename} (open error {err})")
            failed += 1
            continue

        file_size = ctypes.c_uint64()
        if not casc.CascGetFileSize64(h_file, ctypes.byref(file_size)):
            print(f"  SKIP {filename} (size error)")
            casc.CascCloseFile(h_file)
            failed += 1
            continue

        size = file_size.value
        buf = ctypes.create_string_buffer(size)
        bytes_read = ctypes.c_uint32()

        if not casc.CascReadFile(h_file, buf, size, ctypes.byref(bytes_read)):
            err = casc.GetCascError()
            print(f"  SKIP {filename} (read error {err})")
            casc.CascCloseFile(h_file)
            failed += 1
            continue

        casc.CascCloseFile(h_file)

        clean_name = filename.replace("\\", "/")
        if ":" in clean_name:
            clean_name = clean_name.replace(":", "/", 1)
        out_path = output_dir / clean_name
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(buf.raw[:bytes_read.value])
        extracted += 1

    casc.CascCloseStorage(h_storage)
    print(f"\nExtracted {extracted} files to {output_dir}")
    if failed:
        print(f"Failed to extract {failed} files")

    return extracted


def main():
    d2r_default = Path.home() / "Games/bnet/pfx/drive_c/Program Files (x86)/Diablo II Resurrected"
    output_default = SCRIPT_DIR / "work"

    d2r_path = Path(sys.argv[1]) if len(sys.argv) > 1 else d2r_default
    output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else output_default

    print(f"D2R path: {d2r_path}")
    print(f"Output:   {output_dir}")
    print()

    extract_d2r_files(d2r_path, output_dir)


if __name__ == "__main__":
    main()
