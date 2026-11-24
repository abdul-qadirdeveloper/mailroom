from mailroom import read_subscribers, count_total, count_in_group

# My expected answers (from notes/predictions.md, First Check)


def test_total_is_24() -> None:
    text = read_subscribers()
    assert count_total(text) == 24, "expected 24 subscribers in total"


def test_health_curious_has_8() -> None:
    text = read_subscribers()
    assert count_in_group(text, "health-curious") == 8, "expected 8 in health-curious"


def test_casual_movers_has_8() -> None:
    text = read_subscribers()
    assert count_in_group(text, "casual-movers") == 8, "expected 8 in casual-movers"


def test_daily_exercisers_has_8() -> None:
    text = read_subscribers()
    assert count_in_group(text, "daily-exercisers") == 8, "expected 8 in daily-exercisers"
