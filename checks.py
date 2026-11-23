from datetime import date

from mailroom import read_subscribers, count_total, count_in_group, count_joined_since, next_send

text = read_subscribers()

# My expected answers (from notes/predictions.md, First Check)
assert count_total(text) == 24, "expected 24 subscribers in total"
assert count_in_group(text, "health-curious") == 8, "expected 8 in health-curious"
assert count_in_group(text, "casual-movers") == 8, "expected 8 in casual-movers"
assert count_in_group(text, "daily-exercisers") == 8, "expected 8 in daily-exercisers"

# Joined in the last 30 days, run on 2026-11-20: cutoff is 2026-10-21, counted inclusive
run_date = date.fromisoformat("2026-11-20")
assert count_joined_since(text, run_date, 30) == 7, "expected 7 joined since 2026-10-21"

# Next send is the first Monday of the next month
assert next_send(date.fromisoformat("2026-11-20")) == date.fromisoformat("2026-12-07"), "expected 2026-12-07"
assert next_send(date.fromisoformat("2026-12-07")) == date.fromisoformat("2027-01-04"), "expected 2027-01-04"

print("All checks passed.")
