from mailroom import check_footer

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
