from mailroom.checks import check_link

# Rule 4: exactly one main link, written as [Button text](https://...).
# check_link returns a list of problems, empty when there is exactly one link.


def test_one_link_from_issue_01_is_fine() -> None:
    issue = "Hi {{first_name}},\n\n[Download YoYo40+](https://yoyo40plus.example/app)\n\nSee you on your walk."
    assert check_link(issue) == [], "expected no problems (1 link)"


def test_two_links_is_a_problem() -> None:
    issue = (
        "Hi {{first_name}},\n\n"
        "[Download YoYo40+](https://yoyo40plus.example/app)\n\n"
        "See you on your walk.\n\n"
        "[Read the guide](https://yoyo40plus.example/guide)\n"
    )
    assert check_link(issue) == ["Problem: found 2 links, need exactly 1"], "expected a two-links problem"
