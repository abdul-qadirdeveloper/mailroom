# Predictions

## About the newsletter

- My newsletter name is "First Alpha Launch".
- It is for people over 40 age.
- It encourages using our mobile App YoYo40+.

## First Check

There are 24 subscribers in total, 8 in each group.

## Tests First

I expect at least one test per behavior.

## Subject Line Check

Rule 1 in `docs/email-rules.md`: an issue starts with a line `Subject: ...` of 50 characters or fewer.
I count only the text after `Subject: ` (the label itself is not counted).

| # | Subject line in the issue | Characters | What the check should say |
|---|---------------------------|-----------:|---------------------------|
| 1 | `Subject: 10 calm minutes, every day. YoYo40+ is here` (from issue-01) | 43 | `OK: subject is 43 characters` |
| 2 | `Subject: ` (nothing after it) | 0 | `Problem: subject is empty` |
| 3 | `Subject: Your 10-minute walk plan is ready, starting today.` | 50 | `OK: subject is 50 characters` |
| 4 | `Subject: Your 10-minute walk plan is ready, starting today!!` | 51 | `Problem: subject is 51 characters, the limit is 50` |
| 5 | No `Subject:` line at all (the issue starts with `Preview: ...`) | none | `Problem: no Subject line` |
| 6 | `Subject: Your 10-minute walk plan is ready, starting today.` with a hidden `\r` at the end (Windows line ending) | 50 after `strip()` | `OK: subject is 50 characters` |


## Rules 2 to 5 (suggested cases, waiting for my OK)

Claude suggested these. I decide every case and every answer before any test is written.
Each check works like `check_subject`: it returns a list of problems, `[]` when the issue is fine.
"Fine" below means the check returns `[]`.

### Rule 2: Preview line

`Preview: ...` is the second line, 90 characters or fewer. Only the text after `Preview: ` is counted.

| # | Preview line in the issue | Characters | What the check should say |
|---|---------------------------|-----------:|---------------------------|
| 1 | `Preview: 10 minutes a day to support staying strong, active and on your own two feet.` (from issue-01) | 76 | fine |
| 2 | `Preview: 10 minutes a day to support staying strong, active and on your own two feet, from today on.` | 91 | `Problem: preview is 91 characters, the limit is 90` |

### Rule 3: Greeting

The issue greets the reader with `{{first_name}}` (two curly braces on each side).

| # | Greeting line in the issue | What the check should say |
|---|----------------------------|---------------------------|
| 1 | `Hi {{first_name}},` (from issue-01) | fine |
| 2 | `Hi {first_name},` (only one brace on each side, a typo) | `Problem: no {{first_name}} greeting` |

### Rule 4: Exactly one main link

A link is written as `[Button text](https://...)`.

| # | Links in the issue | What the check should say |
|---|--------------------|---------------------------|
| 1 | Only `[Download YoYo40+](https://yoyo40plus.example/app)` (from issue-01) | fine |
| 2 | `[Download YoYo40+](https://yoyo40plus.example/app)` and, further down, `[Read the guide](https://yoyo40plus.example/guide)` | `Problem: found 2 links, need exactly 1` |

### Rule 5: Footer

The issue ends with a line that starts `You're getting this because` and a line that contains `Unsubscribe: {{unsubscribe_url}}`.

| # | Footer in the issue | What the check should say |
|---|---------------------|---------------------------|
| 1 | issue-01 as it is now: `You're getting this because ...` on one line, then `Unsubscribe: {{unsubscribe_url}}` on the last line | fine |
| 2 | `You're getting this because you joined the YoYo40+ waitlist.` and no `Unsubscribe:` anywhere | `Problem: no Unsubscribe line` |
| 3 | `Unsubscribe: {{unsubscribe_url}}` is there, but no line starts `You're getting this because` | `Problem: no "You're getting this because" line` |
| 4 | Both footer lines are missing | `["Problem: no \"You're getting this because\" line", "Problem: no Unsubscribe line"]` (footer order) |
| 5 | `Thanks! You're getting this because you joined.` (not at the start of the line), plus the Unsubscribe line | `Problem: no "You're getting this because" line` |

### Two problems at once

One check runs all five rules and returns every problem it finds, in rule order.

| # | Issue | What the check should say |
|---|-------|---------------------------|
| 1 | issue-01, but the subject is `Your 10-minute walk plan is ready, starting today!!` (51) and the `Unsubscribe:` part is removed | `["Problem: subject is 51 characters, the limit is 50", "Problem: no Unsubscribe line"]` |

## Characters a reader sees versus len()

Text: `👍🏽 Thanks for joining`

| What | Count | Why |
|------|-------|-----|
| Characters a reader sees | 20 | 👍🏽 looks like one character, then a space, then `Thanks for joining` (18) |
| Python `len()` | 21 | 👍🏽 is two code points, thumbs up (U+1F44D) plus a skin-tone modifier (U+1F3FD), so `len()` counts it as 2 |

Checked by running `len()`: it printed 21.

## Moving the code into modules (prediction, nothing moved yet)

All the code is in one file, `src/mailroom/__init__.py` (165 lines). The checks sit at the bottom, after the counting and the dates.

### The move I am predicting for (my plan to confirm)

One file per job, inside `src/mailroom/`:

| New module | What moves into it |
|------------|--------------------|
| `subscribers.py` | `read_subscribers`, `count_total`, `count_in_group`, `count_joined_since` |
| `dates.py` | `next_send` |
| `checks.py` | `check_subject`, `check_preview`, `check_greeting`, `check_link`, `check_footer`, `check_issue` |
| `__init__.py` (stays) | `main`, `read_run_date`, `GROUPS` (the entry point `mailroom:main` in `pyproject.toml` points here) |

### What every test file depends on

Every test file starts with `from mailroom import <name>`. That line looks for the name at the top level of `src/mailroom/__init__.py`. It does not look inside `checks.py` or the other new files. If the name is not at the top level of `__init__.py`, the test file cannot even load.

There are 27 tests in 10 files.

### Prediction

`main` still needs some of the moved functions, so `__init__.py` has to import them back from the new files. Any name `__init__.py` imports sits at its top level again, so `from mailroom import ...` finds it. What breaks depends on which names `main` uses:

| Test file | Imports | Used by `main`? | Breaks? |
|-----------|---------|-----------------|---------|
| `test_counts.py` (4) | `read_subscribers`, `count_total`, `count_in_group` | yes | no |
| `test_joined_since.py` (1) | `read_subscribers`, `count_joined_since` | yes | no |
| `test_next_send.py` (2) | `next_send` | yes | no |
| `test_check_issue.py` (1) | `check_issue` | yes | no |
| `test_main.py` (1) | `main` | stays in `__init__.py` | no |
| `test_check_subject.py` (7) | `check_subject` | no, only `check_issue` calls it | **yes** |
| `test_check_preview.py` (2) | `check_preview` | no | **yes** |
| `test_check_greeting.py` (2) | `check_greeting` | no | **yes** |
| `test_check_link.py` (2) | `check_link` | no | **yes** |
| `test_check_footer.py` (5) | `check_footer` | no | **yes** |

**Five files break, holding 18 tests.** They break because their import line cannot find the name, not because a check gives a wrong answer. The error is an `ImportError` (cannot import name `check_subject` from `mailroom`).

How it will look: pytest loads every test file before it runs any test. When a file cannot load, pytest stops with `Interrupted: 5 errors during collection`. So **none of the 27 tests run**, not even the 9 that would pass.

### What will not break, and why

- **Reading `data/subscribers.csv`.** `read_subscribers` uses the path `data/subscribers.csv`. That path starts from the folder you run the command in (the project folder), not from where the `.py` file sits. Moving the function to `subscribers.py` does not change it.
- **Any expected answer.** Moving code changes where a function lives, not what it returns.

### A break the tests will not catch

`test_main.py` runs `main()` without a command, so it only reaches the `Hello from mailroom!` line. If `__init__.py` forgets to import, say, `check_issue`, every test still passes. The error (`NameError: name 'check_issue' is not defined`) shows up only when someone runs `uv run mailroom check issues/issue-01.md`. After the move, run all three commands by hand too.

### Two ways to fix the 18, my choice

1. Change the import line in the five test files to `from mailroom.checks import check_subject` (and so on). This edits tests, but only the import line, not any expected answer.
2. Leave the tests alone and also import the five single checks in `__init__.py`, even though `main` does not use them.

### What happened

The move I chose was different: `main` went into its own `commands.py` too, and `__init__.py` kept only a comment. So nothing was left at the top level of `__init__.py`, and **all 10 files** failed with `ImportError` (`Interrupted: 10 errors during collection`), not 5. The reason was the one predicted: the import line, not a wrong answer. I used fix 1 (only the import lines changed), and all 27 passed.
