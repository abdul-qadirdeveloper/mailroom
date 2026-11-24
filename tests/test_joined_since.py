from datetime import date

from mailroom import read_subscribers, count_joined_since


# Joined in the last 30 days, run on 2026-11-20: cutoff is 2026-10-21, counted inclusive
def test_joined_in_last_30_days_is_7() -> None:
    text = read_subscribers()
    run_date = date.fromisoformat("2026-11-20")
    assert count_joined_since(text, run_date, 30) == 7, "expected 7 joined since 2026-10-21"
