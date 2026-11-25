import sys
from datetime import date

from mailroom.checks import check_issue
from mailroom.dates import next_send
from mailroom.issue import read_issue
from mailroom.subscribers import GROUPS, count_in_group, count_joined_since, count_total, read_subscribers


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
        problems = check_issue(read_issue(sys.argv[2]))
        if problems == []:
            print("OK")
            sys.exit(0)
        for problem in problems:
            print(problem)
        sys.exit(1)

    if command != "next-send" and command != "subscribers" and command != "check":
        print("Hello from mailroom!")
