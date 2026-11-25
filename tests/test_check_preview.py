from mailroom.checks import check_preview

# Rule 2: the second line is "Preview: ..." of 90 characters or fewer.
# Only the text after "Preview: " is counted.
# check_preview returns a list of problems, empty when the preview is fine.


def test_preview_from_issue_01_is_fine() -> None:
    issue = (
        "Subject: 10 calm minutes, every day. YoYo40+ is here\n"
        "Preview: 10 minutes a day to support staying strong, active and on your own two feet.\n"
    )
    assert check_preview(issue) == [], "expected no problems (76 characters)"


def test_preview_of_91_characters_is_a_problem() -> None:
    issue = (
        "Subject: 10 calm minutes, every day. YoYo40+ is here\n"
        "Preview: 10 minutes a day to support staying strong, active and on your own two feet, from today on.\n"
    )
    assert check_preview(issue) == ["Problem: preview is 91 characters, the limit is 90"], "expected a too-long problem"
