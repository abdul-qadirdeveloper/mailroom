from datetime import date, timedelta


def next_send(run_date: date) -> date:
    # step forward until the month changes: that is the 1st of next month
    day = run_date + timedelta(days=1)
    while day.month == run_date.month:
        day = day + timedelta(days=1)
    # step forward until it is a Monday (weekday 0)
    while day.weekday() != 0:
        day = day + timedelta(days=1)
    return day
