# AGENTS.md

Everything an AI coding agent (Claude Code, Codex, Cursor, and others) needs to know to work on this project. `CLAUDE.md` only points here, so keep this file as the single source of truth.

## What this is

Mailroom is a command-line tool for one newsletter: **First Alpha Launch**. It reads the subscribers, checks an issue, and sends it to a practice mail server.

It grows one step at a time, and each step brings in exactly one new idea, only when the project needs it. The planned steps are:

1. Read the subscribers (and count them).
2. Check an issue before it goes out.
3. Send the issue to a practice mail server.
4. Move Mailroom into the user's existing Email Studio, where its emails are checked with code.

Current state: step 1 is done. `uv run mailroom subscribers` prints the total and one line per group. Dates are added too: `subscribers --since-days 30` and `next-send` (first Monday of next month), both with an optional `--run-date YYYY-MM-DD`. All the code lives in `src/mailroom/__init__.py` (the old `mailroom.py` is gone). The old `checks.py` asserts are now pytest tests, one test per behavior, grouped by behavior in `tests/test_counts.py`, `tests/test_joined_since.py` and `tests/test_next_send.py`; run them with `uv run pytest`.

Step 2 is done too: `uv run mailroom check <issue file>` checks an issue against the five rules in `docs/email-rules.md` (`check_subject`, `check_preview`, `check_greeting`, `check_link` and `check_footer`, all run in rule order by `check_issue`). It prints every problem on its own line and exits 1, or prints `OK` and exits 0. Each check returns a list of problem messages, `[]` when the issue is fine. Length means what Python's `len()` counts (code points), not what a reader sees: `👍🏽 Thanks for joining` is 21, not 20, because 👍🏽 is a thumbs up plus a skin-tone modifier (my decision, proved by `test_emoji_with_skin_tone_counts_as_two_characters`). The cases live in `notes/predictions.md` and the tests in `tests/test_check_*.py`.

## Rules

- Use uv for everything: running, testing, adding packages. Never call `python`, `pip` or `pytest` directly.
- Never use a real person's email address. Use `@example.com` addresses for subscribers and test data, and `@resend.dev` addresses for practice sends.
- Commit and push after every step.
- Keep changes scoped to the current step. Don't add dependencies, frameworks, or abstractions that a later step hasn't asked for yet.
- Make every change directly in the user's laptop folder `D:\Claude\FDE102\mailroom`.
- Behaviors first. I give the expected answers, you write them as pytest tests (one test per behavior, in the `tests/` file for that behavior), show them failing, then write the code that makes them pass.
- I decide the test cases and their answers. Never change an expected answer to make a test pass.
- Never read today's date inside the logic. Pass the run date in as a parameter. Only the command line may read today's date (as the default when `--run-date` is not given).
- When something breaks, show me the full error (the whole traceback, exactly as printed) before changing anything.

## How I learn

- I am new to Python. I have completed up to **13.12** of https://agentfactory.panaversity.org/building-ai-workers/programming-fundamentals/ (update this number as I move on).
- Write only with what I have learned. If something new would really help, stop and tell me its name in one line. I decide.
- When the code uses something new, show me that piece first and ask me to predict what it does. Stay quiet while I guess. Then run it. Explain a line only when I ask.

### What I have learned (lessons 13.1 to 13.12)

- 13.1: values, strings, lists with positions from 0, variables, `print`, predicting before running.
- 13.2: the workbench: tests, the type checker (Pyright, strict mode), linters (ruff), `uv run python file.py`, `uv run pyright`; Git basics (status, diff, log, add, commit, switch -c).
- 13.3: the value kinds `str`, `int`, `float`, `bool`, `None`; type labels like `cents: int`; `#` comments; `+` on text and numbers; `int(...)` to convert text; `ValueError` and `TypeError`; money in whole cents.
- 13.4: `if` / `else`, `==` and comparisons, indentation blocks, `for` loops over a list, filtering inside a loop, a one-line list comprehension filter.
- 13.5: `and`, `or`, `not`; empty values (`""`, `None`, `0`) and the `0` trap; `while` loops and the line that changes their condition.
- 13.6: `def`, parameters with type labels, return types (`-> int`, `-> str`), `return`, pure functions, `assert` with a message.
- 13.7: lists and dictionaries (`dict[str, str]`), keys and values, records, `KeyError`, `.get(key, default)`, `IndexError`, `sorted()` with `key=` and `reverse=True`, CSV rows as records.
- 13.8: text from a file: splitting text into lines with `split("\n")` and into values with `split(",")`, then indexing like `parts[2]`; line endings (`\n`, and the hidden `\r` Windows adds); a leftover `\r` breaks matches (`"open\r"` is not `"open"`); `strip()` to clean both ends; values read from a file are still text. Recognize only (not taught in depth): `Path("...").read_text(encoding="utf-8")` to read a whole file into a string.
- 13.9: dates: comparing dates as ISO text (`YYYY-MM-DD`) and why other formats like `3/10/2027` compare wrongly; `date` (a calendar day) versus `datetime` (a moment that can shift with time zones); `from datetime import date, timedelta`; `date.fromisoformat("2027-01-25")`; adding days with `date + timedelta(days=45)`; month-end, year-end and leap-year rollover; doing date math with calendar days or UTC, not local time.
- 13.10: reading an error: a Python traceback is read from the bottom up; the last line is the error kind (a word ending in `Error`) and its message, the failing line is just above it with `line N` and a row of `^` under the failing part, and the oldest call is at the top; skip `<frozen runpy>` lines; examples `KeyError: 'terms'` and `IndexError`; telling the line that made a bad value from the line it was handed to. Recognize only (not taught in depth): Node/TypeScript stack traces (`at` lines, `node:internal` frames, `throw new Error(...)`).
- 13.11: tests first, the TDG (Test-Driven Generation) loop: I decide the cases and expected answers, the agent writes them as tests, they run and fail, the agent writes the code, they run again and pass; tests as the specification, one required behavior per test; a new test must fail for the right reason (the code is missing, not a typo in the test); I own every expected value and read every test against my list; the agent never edits tests to make them pass (check with `git diff <commit> -- tests/` showing nothing); commit the failing tests first so history shows tests came before code; passing is evidence for the chosen inputs, not proof, so pick cases like a month end, a year end, a leap day and an input that must fail. Recognize only (not taught in depth): pytest as the test runner, named tests, `with pytest.raises(...)` to check a call raises an error, TypeScript `test("name", () => {...})` and `assert.equal` / `assert.throws`.
- 13.12: judgment (no new Python syntax): a function signature as a contract (`list[str]`, `bool`); turning a vague goal into rules written as input and output examples; reading a rule as a sentence to catch bugs like `>=` that includes the boundary value; red-teaming inputs (empty file, zero amount, missing column, text where a number belongs), e.g. `int("")` raises `ValueError`; asking "what input would break this?" and deciding which answers become tests; if a piece is hard to test it does too much, so split it, and if you cannot write a test for it, it is not specified yet; reading the diff before every commit (did a test change, was a package added, is its name real); checking lightly versus reading every line (private data, money movement, long code).

Also met in this project (step 1, subscriber counts): `from mailroom import ...` to use functions from another file, and `sys.argv` for the words typed after the command. Dates step: `date - timedelta(...)`, `date.today()` (command line only), `.month` and `.weekday()` (0 is Monday). Tests step: plain pytest test functions (`def test_...() -> None:` holding an `assert`), run with `uv run pytest`. Issue-check step: `"text" in other_text` to find text inside text, `+` to join two lists, and `sys.exit(0)` / `sys.exit(1)` to set the exit code (the program stops on that line).

Not learned yet, so each one is "something new": `pathlib` / `Path` / `read_text` beyond recognizing the one line, `open()` and `with`, the `csv` module, `try` / `except` and `raise` (13.10 only reads errors and 13.11 only shows `pytest.raises`; neither teaches handling or raising them), `pytest.raises` beyond recognizing it (13.11 only shows it), `-> None` beyond test functions and `main`, `break` / `continue`, default parameter values, docstrings, classes and objects, dataclasses. The starter code already uses `-> None`, `import` and a pytest test function; treat them as new the first time they matter.

## Commands

The project uses [uv](https://docs.astral.sh/uv/) and Python 3.14 (pinned in `.python-version`).

```bash
uv sync                                   # create .venv and install dependencies
uv run mailroom subscribers               # run the CLI (entry point: mailroom:main)
uv run mailroom next-send --run-date 2026-11-20
uv run mailroom check issues/issue-01.md  # prints OK (exit 0) or each problem (exit 1)
uv run pytest                             # run all tests
uv run pytest tests/test_main.py::test_main_prints_greeting   # run one test
uv add <pkg>                              # add a runtime dependency
uv add --dev <pkg>                        # add a dev-only dependency
```

No type checker, linter or formatter is configured yet.

## Layout

- `src/mailroom/` is the package (src layout, built with `uv_build`). The `mailroom` console script in `pyproject.toml` points at `mailroom:main` in `__init__.py`.
- `tests/` holds pytest tests. pytest is the only dev dependency.
- `uv.lock` is committed; update it through `uv add` / `uv sync`, not by hand.
- `.venv` is not shared between machines; run `uv sync` to create it.

## Where the code lives

- The user's laptop (Windows): `D:\Claude\FDE102\mailroom`, next to `D:\Claude\FDE102\my-email-studio` (the Email Studio for step 4).
- GitHub (public): https://github.com/abdul-qadirdeveloper/mailroom, branch `main`. The laptop folder tracks `origin/main`.
