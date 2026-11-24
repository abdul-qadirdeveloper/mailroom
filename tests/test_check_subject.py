from mailroom import check_subject

# Rule 1: an issue starts with a line "Subject: ..." of 50 characters or fewer.
# Only the text after "Subject: " is counted.
# check_subject returns a list of problems, empty when the subject is fine.


def test_subject_from_issue_01_is_fine() -> None:
    issue = "Subject: 10 calm minutes, every day. YoYo40+ is here\nPreview: 10 minutes a day."
    assert check_subject(issue) == [], "expected no problems (43 characters)"


def test_empty_subject_is_a_problem() -> None:
    issue = "Subject: \nPreview: 10 minutes a day."
    assert check_subject(issue) == ["Problem: subject is empty"], "expected an empty-subject problem"


def test_subject_of_exactly_50_characters_is_fine() -> None:
    issue = "Subject: Your 10-minute walk plan is ready, starting today.\nPreview: 10 minutes a day."
    assert check_subject(issue) == [], "expected no problems (50 characters)"


def test_subject_of_51_characters_is_a_problem() -> None:
    issue = "Subject: Your 10-minute walk plan is ready, starting today!!\nPreview: 10 minutes a day."
    assert check_subject(issue) == ["Problem: subject is 51 characters, the limit is 50"], "expected a too-long problem"


def test_issue_with_no_subject_line_is_a_problem() -> None:
    issue = "Preview: 10 minutes a day.\n\nHi {{first_name}},"
    assert check_subject(issue) == ["Problem: no Subject line"], "expected a no-Subject-line problem"


def test_hidden_windows_line_ending_does_not_count() -> None:
    issue = "Subject: Your 10-minute walk plan is ready, starting today.\r\nPreview: 10 minutes a day."
    assert check_subject(issue) == [], "expected no problems (50 characters once the \\r is removed)"


def test_emoji_with_skin_tone_counts_as_two_characters() -> None:
    # a reader sees 50 characters, but len() counts 👍🏽 as 2 (thumbs up + skin tone), so 51
    issue = "Subject: 👍🏽 Thanks for joining First Alpha Launch, see you!!\nPreview: 10 minutes a day."
    assert check_subject(issue) == ["Problem: subject is 51 characters, the limit is 50"], "expected len() to count 51"
