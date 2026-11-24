from mailroom import check_greeting

# Rule 3: the issue greets the reader with {{first_name}} (two braces on each side).
# check_greeting returns a list of problems, empty when the greeting is fine.


def test_greeting_from_issue_01_is_fine() -> None:
    issue = "Subject: Hello\nPreview: Hello\n\nHi {{first_name}},\n\nYou move when you can."
    assert check_greeting(issue) == [], "expected no problems"


def test_greeting_with_single_braces_is_a_problem() -> None:
    issue = "Subject: Hello\nPreview: Hello\n\nHi {first_name},\n\nYou move when you can."
    assert check_greeting(issue) == ["Problem: no {{first_name}} greeting"], "expected a no-greeting problem"
