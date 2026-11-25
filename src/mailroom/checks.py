def check_subject(issue_text: str) -> list[str]:
    # the first line must be "Subject: ..." with 50 characters or fewer after the label
    first_line = issue_text.split("\n")[0].strip()
    if not first_line.startswith("Subject:"):
        return ["Problem: no Subject line"]
    subject = first_line.split("Subject:")[1].strip()
    if subject == "":
        return ["Problem: subject is empty"]
    if len(subject) > 50:
        return ["Problem: subject is " + str(len(subject)) + " characters, the limit is 50"]
    return []


def check_preview(issue_text: str) -> list[str]:
    # the second line must be "Preview: ..." with 90 characters or fewer after the label
    lines = issue_text.split("\n")
    if len(lines) < 2 or not lines[1].strip().startswith("Preview:"):
        return ["Problem: no Preview line"]
    preview = lines[1].strip().split("Preview:")[1].strip()
    if len(preview) > 90:
        return ["Problem: preview is " + str(len(preview)) + " characters, the limit is 90"]
    return []


def check_greeting(issue_text: str) -> list[str]:
    # the reader must be greeted with {{first_name}}
    if "{{first_name}}" in issue_text:
        return []
    return ["Problem: no {{first_name}} greeting"]


def check_link(issue_text: str) -> list[str]:
    # there must be exactly one link written as [Button text](https://...)
    links = 0
    for line in issue_text.split("\n"):
        if "](https://" in line:
            links = links + 1
    if links != 1:
        return ["Problem: found " + str(links) + " links, need exactly 1"]
    return []


def check_footer(issue_text: str) -> list[str]:
    # some line must start "You're getting this because",
    # and some line must contain "Unsubscribe: {{unsubscribe_url}}"
    problems: list[str] = []
    has_getting_line = False
    for line in issue_text.split("\n"):
        if line.strip().startswith("You're getting this because"):
            has_getting_line = True
    if not has_getting_line:
        problems = problems + ["Problem: no \"You're getting this because\" line"]
    if "Unsubscribe: {{unsubscribe_url}}" not in issue_text:
        problems = problems + ["Problem: no Unsubscribe line"]
    return problems


def check_issue(issue_text: str) -> list[str]:
    # run every rule, in rule order, and keep every problem
    return (
        check_subject(issue_text)
        + check_preview(issue_text)
        + check_greeting(issue_text)
        + check_link(issue_text)
        + check_footer(issue_text)
    )
