"""Log file analyzer — streams a log file, summarizes severity levels,
timestamp range, and top recurring messages. Demonstrates generators,
decorators, and regex parsing on a real-world-ish log format."""

import re
import sys
from collections import Counter
from datetime import datetime
from functools import wraps
from pathlib import Path
from typing import Iterator

LOG_PATTERN = re.compile(
    r"^(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) "
    r"\[(?P<level>\w+)\] (?P<message>.+)$"
)


def timer(func):
    """Decorator that prints how long a function took to run."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = datetime.now()
        result = func(*args, **kwargs)
        elapsed = (datetime.now() - start).total_seconds()
        print(f"[{func.__name__}] took {elapsed:.4f}s")
        return result
    return wrapper


def read_lines(path: str) -> Iterator[str]:
    """Yield lines one at a time — constant memory, even for huge files."""
    with open(path, encoding="utf-8", errors="ignore") as f:
        for line in f:
            yield line.rstrip("\n")


@timer
def analyse(path: str) -> None:
    levels = Counter()
    messages = Counter()
    timestamps = []
    unparsed = 0

    for line in read_lines(path):
        match = LOG_PATTERN.match(line)
        if not match:
            if line.strip():
                unparsed += 1
            continue

        levels[match["level"]] += 1
        messages[match["message"]] += 1
        timestamps.append(match["timestamp"])

    if not timestamps:
        print("No recognizable log lines found.")
        return

    print(f"\n{path}")
    print(f"Time range: {timestamps[0]} -> {timestamps[-1]}\n")

    print("Level counts:")
    for level, count in levels.most_common():
        print(f"  {level:10} {count}")

    print("\nTop recurring messages:")
    for message, count in messages.most_common(5):
        print(f"  {count:4}x  {message}")

    if unparsed:
        print(f"\n({unparsed} lines didn't match the expected log format)")


def main() -> None:
    path = sys.argv[1] if len(sys.argv) >= 2 else input("Path to log file: ").strip()

    if not Path(path).is_file():
        print(f"File not found: {path}")
        sys.exit(1)

    analyse(path)


if __name__ == "__main__":
    main()
