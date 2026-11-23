from mailroom import read_subscribers, count_total, count_in_group

text = read_subscribers()

# My expected answers (from notes/predictions.md, First Check)
assert count_total(text) == 24, "expected 24 subscribers in total"
assert count_in_group(text, "health-curious") == 8, "expected 8 in health-curious"
assert count_in_group(text, "casual-movers") == 8, "expected 8 in casual-movers"
assert count_in_group(text, "daily-exercisers") == 8, "expected 8 in daily-exercisers"

print("All checks passed.")
