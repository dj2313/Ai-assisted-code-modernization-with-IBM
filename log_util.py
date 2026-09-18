# log_util.py
# A simple timestamp logger for KM-Waechter.
# Modernized 2024: removed dead DEBUG branch, use list.clear(), f-string.

import time

LOG_LINES: list[str] = []   # module-level buffer; cleared by flush_log after each nightly run


def log(message: str) -> None:
    """Append a timestamped line to the in-memory log and print it."""
    stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{stamp}] {message}"
    LOG_LINES.append(line)
    print(line)


def flush_log(path: str) -> None:
    """Write all buffered log lines to *path* (append mode) and clear the buffer."""
    with open(path, "a") as f:
        for line in LOG_LINES:
            f.write(line + "\n")
    LOG_LINES.clear()
