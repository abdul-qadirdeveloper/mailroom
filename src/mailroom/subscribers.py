from datetime import date, timedelta
from pathlib import Path

GROUPS: list[str] = ["health-curious", "casual-movers", "daily-exercisers"]


def read_subscribers() -> str:
    return Path("data/subscribers.csv").read_text(encoding="utf-8")


def count_total(text: str) -> int:
    lines = text.strip().split("\n")
    return len(lines) - 1  # the first line is the header, not a subscriber


def count_in_group(text: str, group: str) -> int:
    count = 0
    for line in text.strip().split("\n"):
        parts = line.strip().split(",")
        if parts[3] == group:
            count = count + 1
    return count


def count_joined_since(text: str, run_date: date, days: int) -> int:
    cutoff = run_date - timedelta(days=days)
    count = 0
    for line in text.strip().split("\n"):
        parts = line.strip().split(",")
        if parts[4] != "joined_on":  # skip the header line
            joined = date.fromisoformat(parts[4])
            if joined >= cutoff:
                count = count + 1
    return count
