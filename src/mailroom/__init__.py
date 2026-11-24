import sys
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


def next_send(run_date: date) -> date:
    # step forward until the month changes: that is the 1st of next month
    day = run_date + timedelta(days=1)
    while day.month == run_date.month:
        day = day + timedelta(days=1)
    # step forward until it is a Monday (weekday 0)
    while day.weekday() != 0:
        day = day + timedelta(days=1)
    return day


def check_subject(issue_text: str) -> list[str]:
    # the first line must be "Subject: ..." with 50 characters or fewer after the label
    first_line = issue_text.split("\n")[0].strip()
    if not first_line.startswith("Subject:"):
        return ["Problem: no Subject line"]
    subject = first_line.split("Subject:")[1].strip()
    if subject == "":
        return ["Problem: subject is empty"]
    if len(subject) > 50:
        return ["Problem: subject is " + str(len(subject)) + " characters, the limit is 50"]
    return []


def check_preview(issue_text: str) -> list[str]:
    # the second line must be "Preview: ..." with 90 characters or fewer after the label
    lines = issue_text.split("\n")
    if len(lines) < 2 or not lines[1].strip().startswith("Preview:"):
        return ["Problem: no Preview line"]
    preview = lines[1].strip().split("Preview:")[1].strip()
    if len(preview) > 90:
        return ["Problem: preview is " + str(len(preview)) + " characters, the limit is 90"]
    return []


def check_greeting(issue_text: str) -> list[str]:
    # the reader must be greeted with {{first_name}}
    if "{{first_name}}" in issue_text:
        return []
    return ["Problem: no {{first_name}} greeting"]


def check_link(issue_text: str) -> list[str]:
    # there must be exactly one link written as [Button text](https://...)
    links = 0
    for line in issue_text.split("\n"):
        if "](https://" in line:
            links = links + 1
    if links != 1:
        return ["Problem: found " + str(links) + " links, need exactly 1"]
    return []


def check_footer(issue_text: str) -> list[str]:
    # some line must start "You're getting this because",
    # and some line must contain "Unsubscribe: {{unsubscribe_url}}"
    problems: list[str] = []
    has_getting_line = False
    for line in issue_text.split("\n"):
        if line.strip().startswith("You're getting this because"):
            has_getting_line = True
    if not has_getting_line:
        problems = problems + ["Problem: no \"You're getting this because\" line"]
    if "Unsubscribe: {{unsubscribe_url}}" not in issue_text:
        problems = problems + ["Problem: no Unsubscribe line"]
    return problems


def check_issue(issue_text: str) -> list[str]:
    # run every rule, in rule order, and keep every problem
    return (
        check_subject(issue_text)
        + check_preview(issue_text)
        + check_greeting(issue_text)
        + check_link(issue_text)
        + check_footer(issue_text)
    )


def read_run_date() -> date:
    # the command line is the only place that may read today's date
    run_date = date.today()
    i = 2
    while i < len(sys.argv) - 1:
        if sys.argv[i] == "--run-date":
            run_date = date.fromisoformat(sys.argv[i + 1])
        i = i + 1
    return run_date


def main() -> None:
    command = ""
    if len(sys.argv) > 1:
        command = sys.argv[1]

    if command == "next-send":
        print("Next send:", next_send(read_run_date()))

    if command == "subscribers":
        text = read_subscribers()
        print("Total:", count_total(text))
        for group in GROUPS:
            print(group + ":", count_in_group(text, group))

        # Optional: --since-days 30 --run-date 2026-11-20
        since_days = 0
        i = 2
        while i < len(sys.argv) - 1:
            if sys.argv[i] == "--since-days":
                since_days = int(sys.argv[i + 1])
            i = i + 1
        if since_days > 0:
            print("Joined in the last", since_days, "days:", count_joined_since(text, read_run_date(), since_days))

    if command == "check":
        if len(sys.argv) < 3:
            print("Usage: mailroom check <issue file>")
            sys.exit(1)
        problems = check_issue(Path(sys.argv[2]).read_text(encoding="utf-8"))
        if problems == []:
            print("OK")
            sys.exit(0)
        for problem in problems:
            print(problem)
        sys.exit(1)

    if command != "next-send" and command != "subscribers" and command != "check":
        print("Hello from mailroom!")
