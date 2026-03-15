import ctypes
import sys
from pathlib import Path

MAX_PATH = 1024
MD5_HASH_SIZE = 16
CASC_LOCALE_ALL = 0xFFFFFFFF
CASC_OPEN_BY_NAME = 0x00000000

SCRIPT_DIR = Path(__file__).parent
CASCLIB_PATH = SCRIPT_DIR / "CascLib" / "build" / "libcasc.so"


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


def load_casclib():
    if not CASCLIB_PATH.exists():
        sys.exit(f"Error: CascLib not found at {CASCLIB_PATH}\n"
                 "Build it first: cd CascLib/build && cmake .. && make")

    lib = ctypes.CDLL(str(CASCLIB_PATH))

    lib.CascOpenStorage.argtypes = [ctypes.c_char_p, ctypes.c_uint32, ctypes.POINTER(ctypes.c_void_p)]
    lib.CascOpenStorage.restype = ctypes.c_bool

    lib.CascCloseStorage.argtypes = [ctypes.c_void_p]
    lib.CascCloseStorage.restype = ctypes.c_bool

    lib.CascFindFirstFile.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.POINTER(CASC_FIND_DATA), ctypes.c_char_p]
    lib.CascFindFirstFile.restype = ctypes.c_void_p

    lib.CascFindNextFile.argtypes = [ctypes.c_void_p, ctypes.POINTER(CASC_FIND_DATA)]
    lib.CascFindNextFile.restype = ctypes.c_bool

    lib.CascFindClose.argtypes = [ctypes.c_void_p]
    lib.CascFindClose.restype = ctypes.c_bool

    lib.CascOpenFile.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_uint32, ctypes.c_uint32, ctypes.POINTER(ctypes.c_void_p)]
    lib.CascOpenFile.restype = ctypes.c_bool

    lib.CascGetFileSize64.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint64)]
    lib.CascGetFileSize64.restype = ctypes.c_bool

    lib.CascReadFile.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint32)]
    lib.CascReadFile.restype = ctypes.c_bool

    lib.CascCloseFile.argtypes = [ctypes.c_void_p]
    lib.CascCloseFile.restype = ctypes.c_bool

    lib.GetCascError.argtypes = []
    lib.GetCascError.restype = ctypes.c_uint32

    return lib


def open_storage(lib, d2r_path):
    storage_path = d2r_path / "Data"
    if not storage_path.exists():
        sys.exit(f"Error: D2R Data directory not found at {storage_path}")

    h_storage = ctypes.c_void_p()
    if not lib.CascOpenStorage(str(storage_path).encode("utf-8"), CASC_LOCALE_ALL, ctypes.byref(h_storage)):
        err = lib.GetCascError()
        sys.exit(f"Error: Failed to open CASC storage at {storage_path} (error {err})")

    print(f"Opened CASC storage: {storage_path}")
    return h_storage


def find_files(lib, h_storage, path_contains, suffix):
    find_data = CASC_FIND_DATA()
    matching = []

    h_find = lib.CascFindFirstFile(h_storage, b"*", ctypes.byref(find_data), None)
    if not h_find or h_find == ctypes.c_void_p(-1).value:
        sys.exit("Error: CascFindFirstFile failed")

    while True:
        filename = find_data.szFileName.decode("utf-8", errors="replace")
        normalized = filename.replace("\\", "/").lower()
        if path_contains in normalized and normalized.endswith(suffix):
            matching.append(filename)

        if not lib.CascFindNextFile(h_find, ctypes.byref(find_data)):
            break

    lib.CascFindClose(h_find)
    return matching


def read_file(lib, h_storage, filename):
    h_file = ctypes.c_void_p()
    if not lib.CascOpenFile(h_storage, filename.encode("utf-8"), 0, CASC_OPEN_BY_NAME, ctypes.byref(h_file)):
        return None

    file_size = ctypes.c_uint64()
    if not lib.CascGetFileSize64(h_file, ctypes.byref(file_size)):
        lib.CascCloseFile(h_file)
        return None

    size = file_size.value
    buf = ctypes.create_string_buffer(size)
    bytes_read = ctypes.c_uint32()

    if not lib.CascReadFile(h_file, buf, size, ctypes.byref(bytes_read)):
        lib.CascCloseFile(h_file)
        return None

    lib.CascCloseFile(h_file)
    return buf.raw[:bytes_read.value]


def normalize_casc_path(filename):
    clean = filename.replace("\\", "/")
    if ":" in clean:
        clean = clean.replace(":", "/", 1)
    return clean


def extract_d2r_files(d2r_path: Path, output_dir: Path):
    lib = load_casclib()
    h_storage = open_storage(lib, d2r_path)

    matching_files = find_files(lib, h_storage, "data/global/excel/", ".txt")
    print(f"Found {len(matching_files)} excel .txt files")

    if not matching_files:
        print("No matching files found. Listing some files from storage to debug:")
        all_files = find_files(lib, h_storage, "", "")
        for f in all_files[:50]:
            print(f"  {f}")
        lib.CascCloseStorage(h_storage)
        sys.exit(1)

    extracted = 0
    failed = 0
    for filename in sorted(matching_files):
        data = read_file(lib, h_storage, filename)
        if data is None:
            print(f"  SKIP {filename}")
            failed += 1
            continue

        out_path = output_dir / normalize_casc_path(filename)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(data)
        extracted += 1

    lib.CascCloseStorage(h_storage)
    print(f"\nExtracted {extracted} files to {output_dir}")
    if failed:
        print(f"Failed to extract {failed} files")

    return extracted


def main():
    from platform_utils import get_d2r_path
    output_default = SCRIPT_DIR / "work"

    d2r_path = Path(sys.argv[1]) if len(sys.argv) > 1 else get_d2r_path()
    output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else output_default

    print(f"D2R path: {d2r_path}")
    print(f"Output:   {output_dir}")
    print()

    extract_d2r_files(d2r_path, output_dir)


if __name__ == "__main__":
    main()
