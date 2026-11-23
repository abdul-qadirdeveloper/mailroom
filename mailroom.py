import sys
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


if len(sys.argv) > 1 and sys.argv[1] == "subscribers":
    text = read_subscribers()
    print("Total:", count_total(text))
    for group in GROUPS:
        print(group + ":", count_in_group(text, group))
