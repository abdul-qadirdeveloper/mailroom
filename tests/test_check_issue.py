from mailroom.checks import check_issue

# check_issue runs all five rules and returns every problem, in rule order.


def test_issue_with_two_problems_returns_both_in_rule_order() -> None:
    issue = (
        "Subject: Your 10-minute walk plan is ready, starting today!!\n"
        "Preview: 10 minutes a day to support staying strong, active and on your own two feet.\n"
        "\n"
        "Hi {{first_name}},\n"
        "\n"
        "[Download YoYo40+](https://yoyo40plus.example/app)\n"
        "\n"
        "See you on your walk.\n"
        "\n"
        "You're getting this because you joined the YoYo40+ waitlist. YoYo40+, {{company_address}} · \n"
    )
    assert check_issue(issue) == [
        "Problem: subject is 51 characters, the limit is 50",
        "Problem: no Unsubscribe line",
    ], "expected the subject problem, then the footer problem"
