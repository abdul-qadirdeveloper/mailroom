from mailroom.checks import check_footer

# Rule 5: the issue ends with a line that starts "You're getting this because"
# and a line that contains "Unsubscribe: {{unsubscribe_url}}".
# check_footer returns a list of problems, empty when the footer is fine.


def test_two_line_footer_from_issue_01_is_fine() -> None:
    issue = (
        "See you on your walk.\n\n"
        "You're getting this because you joined the YoYo40+ waitlist. YoYo40+, {{company_address}} · \n"
        "Unsubscribe: {{unsubscribe_url}}"
    )
    assert check_footer(issue) == [], "expected no problems"


def test_footer_without_unsubscribe_is_a_problem() -> None:
    issue = "See you on your walk.\n\nYou're getting this because you joined the YoYo40+ waitlist."
    assert check_footer(issue) == ["Problem: no Unsubscribe line"], "expected a no-Unsubscribe problem"


def test_footer_without_getting_this_line_is_a_problem() -> None:
    issue = "See you on your walk.\n\nUnsubscribe: {{unsubscribe_url}}"
    assert check_footer(issue) == [
        "Problem: no \"You're getting this because\" line"
    ], "expected a no-getting-this-because problem"


def test_footer_with_both_lines_missing_gives_two_problems() -> None:
    issue = "See you on your walk."
    assert check_footer(issue) == [
        "Problem: no \"You're getting this because\" line",
        "Problem: no Unsubscribe line",
    ], "expected both footer problems, in footer order"


def test_getting_this_words_mid_line_do_not_count() -> None:
    issue = (
        "See you on your walk.\n\n"
        "Thanks! You're getting this because you joined.\n"
        "Unsubscribe: {{unsubscribe_url}}"
    )
    assert check_footer(issue) == [
        "Problem: no \"You're getting this because\" line"
    ], "expected a no-getting-this-because problem"
