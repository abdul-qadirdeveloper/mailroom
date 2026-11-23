# AGENTS.md

Everything an AI coding agent (Claude Code, Codex, Cursor, and others) needs to know to work on this project. `CLAUDE.md` only points here, so keep this file as the single source of truth.

## What this is

Mailroom is a command-line tool for one newsletter: **First Alpha Launch**. It reads the subscribers, checks an issue, and sends it to a practice mail server.

It grows one step at a time, and each step brings in exactly one new idea, only when the project needs it. The planned steps are:

1. Read the subscribers (and count them).
2. Check an issue before it goes out.
3. Send the issue to a practice mail server.
4. Move Mailroom into the user's existing Email Studio, where its emails are checked with code.

Current state: step 1 is done. `uv run mailroom.py subscribers` prints the total and one line per group, and `uv run checks.py` checks those counts with asserts.

## Rules

- Use uv for everything: running, testing, adding packages. Never call `python`, `pip` or `pytest` directly.
- Never use a real person's email address. Use `@example.com` addresses for subscribers and test data, and `@resend.dev` addresses for practice sends.
- Commit and push after every step.
- Keep changes scoped to the current step. Don't add dependencies, frameworks, or abstractions that a later step hasn't asked for yet.
- Make every change directly in the user's laptop folder `D:\Claude\FDE102\mailroom`.
- Behaviors first. I give the expected answers, you write them as checks (assert lines in `checks.py`), show them failing, then write the code that makes them pass.

## How I learn

- I am new to Python. I have completed up to **13.9** of https://agentfactory.panaversity.org/building-ai-workers/programming-fundamentals/ (update this number as I move on).
- Write only with what I have learned. If something new would really help, stop and tell me its name in one line. I decide.
- When the code uses something new, show me that piece first and ask me to predict what it does. Stay quiet while I guess. Then run it. Explain a line only when I ask.

### What I have learned (lessons 13.1 to 13.9)

- 13.1: values, strings, lists with positions from 0, variables, `print`, predicting before running.
- 13.2: the workbench: tests, the type checker (Pyright, strict mode), linters (ruff), `uv run python file.py`, `uv run pyright`; Git basics (status, diff, log, add, commit, switch -c).
- 13.3: the value kinds `str`, `int`, `float`, `bool`, `None`; type labels like `cents: int`; `#` comments; `+` on text and numbers; `int(...)` to convert text; `ValueError` and `TypeError`; money in whole cents.
- 13.4: `if` / `else`, `==` and comparisons, indentation blocks, `for` loops over a list, filtering inside a loop, a one-line list comprehension filter.
- 13.5: `and`, `or`, `not`; empty values (`""`, `None`, `0`) and the `0` trap; `while` loops and the line that changes their condition.
- 13.6: `def`, parameters with type labels, return types (`-> int`, `-> str`), `return`, pure functions, `assert` with a message.
- 13.7: lists and dictionaries (`dict[str, str]`), keys and values, records, `KeyError`, `.get(key, default)`, `IndexError`, `sorted()` with `key=` and `reverse=True`, CSV rows as records.
- 13.8: text from a file: splitting text into lines with `split("\n")` and into values with `split(",")`, then indexing like `parts[2]`; line endings (`\n`, and the hidden `\r` Windows adds); a leftover `\r` breaks matches (`"open\r"` is not `"open"`); `strip()` to clean both ends; values read from a file are still text. Recognize only (not taught in depth): `Path("...").read_text(encoding="utf-8")` to read a whole file into a string.
- 13.9: dates: comparing dates as ISO text (`YYYY-MM-DD`) and why other formats like `3/10/2027` compare wrongly; `date` (a calendar day) versus `datetime` (a moment that can shift with time zones); `from datetime import date, timedelta`; `date.fromisoformat("2027-01-25")`; adding days with `date + timedelta(days=45)`; month-end, year-end and leap-year rollover; doing date math with calendar days or UTC, not local time.

Also met in this project (step 1, subscriber counts): `from mailroom import ...` to use functions from another file, and `sys.argv` for the words typed after the command.

Not learned yet, so each one is "something new": `pathlib` / `Path` / `read_text` beyond recognizing the one line, `open()` and `with`, the `csv` module, `try` / `except` (13.10), named test functions and pytest (13.11), `-> None`, `break` / `continue`, default parameter values, docstrings, classes and objects, dataclasses. The starter code already uses `-> None`, `import` and a pytest test function; treat them as new the first time they matter.

## Commands

The project uses [uv](https://docs.astral.sh/uv/) and Python 3.14 (pinned in `.python-version`).

```bash
uv sync                                   # create .venv and install dependencies
uv run mailroom                           # run the CLI (entry point: mailroom:main)
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
