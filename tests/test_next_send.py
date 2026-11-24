from datetime import date

from mailroom import next_send

# Next send is the first Monday of the next month


def test_next_send_mid_month() -> None:
    assert next_send(date.fromisoformat("2026-11-20")) == date.fromisoformat("2026-12-07"), "expected 2026-12-07"


def test_next_send_crosses_year_end() -> None:
    assert next_send(date.fromisoformat("2026-12-07")) == date.fromisoformat("2027-01-04"), "expected 2027-01-04"
