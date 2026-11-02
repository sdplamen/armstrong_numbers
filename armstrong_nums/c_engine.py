"""Loads the C engine (c_ext/armstrong.c) with ctypes, compiling it on first use if needed."""
import ctypes
import os
import shutil
import subprocess
import tempfile
import threading
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / 'c_ext' / 'armstrong.c'
LIBRARY = SOURCE.with_suffix('.so')

_lib = None
_lock = threading.Lock()


class CEngineUnavailable(RuntimeError):
    pass


def build():
    compiler = os.environ.get('CC') or shutil.which('cc') or shutil.which('gcc')
    if not compiler:
        raise CEngineUnavailable('No C compiler found to build the C engine.')

    # Build to a temp file and move it into place, so parallel workers never load a half-written library.
    fd, tmp_path = tempfile.mkstemp(suffix='.so', dir=LIBRARY.parent)
    os.close(fd)
    try:
        subprocess.run([compiler, '-O2', '-shared', '-fPIC', '-o', tmp_path, str(SOURCE)],
                       check=True, capture_output=True, text=True)
        os.replace(tmp_path, LIBRARY)
    except subprocess.CalledProcessError as e:
        raise CEngineUnavailable(f'Failed to build the C engine: {e.stderr.strip()}') from e
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def _load():
    global _lib
    with _lock:
        if _lib is None:
            if not LIBRARY.exists() or LIBRARY.stat().st_mtime < SOURCE.stat().st_mtime:
                build()
            lib = ctypes.CDLL(str(LIBRARY))
            lib.armstrong_numbers_in_range.argtypes = [
                ctypes.c_uint64, ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64), ctypes.c_size_t,
            ]
            lib.armstrong_numbers_in_range.restype = ctypes.c_size_t
            _lib = lib
    return _lib


def is_available():
    try:
        _load()
        return True
    except (CEngineUnavailable, OSError):
        return False


def find_armstrong_numbers(start, end):
    lib = _load()
    capacity = 128  # there are only 51 Armstrong numbers below 2^64
    while True:
        buffer = (ctypes.c_uint64 * capacity)()
        count = lib.armstrong_numbers_in_range(start, end, buffer, capacity)
        if count <= capacity:
            return list(buffer[:count])
        capacity = count
