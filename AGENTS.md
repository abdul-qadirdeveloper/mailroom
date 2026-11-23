# AGENTS.md

Everything an AI coding agent (Claude Code, Codex, Cursor, and others) needs to know to work on this project. `CLAUDE.md` only points here, so keep this file as the single source of truth.

## What this is

Mailroom is a small Python tool for a newsletter. It is a learning project: it grows one step at a time, and each step brings in exactly one new idea, only when the project needs it. The planned steps are:

1. Count subscribers.
2. Check an issue before it goes out.
3. Send the issue to a practice mail server (a local test SMTP server, never a real one).
4. Move Mailroom into the user's existing Email Studio, where its emails are checked with code.

Current state: the project is scaffolded only. `main()` prints a greeting and one test checks it. Step 1 has not started.

## How to work here

- Keep changes scoped to the current step. Don't add dependencies, frameworks, or abstractions that a later step hasn't asked for yet.
- When a step introduces a new idea, say what it is and why the project needs it now.
- Never send email to a real mail server or real addresses. Step 3 uses a local practice server only.
- Make every change directly in the user's laptop folder `D:\Claude\FDE102\mailroom`.

## Learning rules

The user is learning programming fundamentals by building this project, following Chapter 13 of the Agent Factory course: https://agentfactory.panaversity.org/building-ai-workers/programming-fundamentals/

**Current lesson: 13.7 (Lists and dictionaries).** Update this line when the user moves on; the next lesson is 13.8 (Text from a file).

### Concepts the user has learned (lessons 13.1 to 13.7)

- 13.1: values, strings, lists with positions from 0, variables, `print`, predicting before running.
- 13.2: the workbench: tests, the type checker (Pyright, strict mode), linters (ruff), `uv run python file.py`, `uv run pyright`; Git basics (status, diff, log, add, commit, switch -c).
- 13.3: the value kinds `str`, `int`, `float`, `bool`, `None`; type labels like `cents: int`; `#` comments; `+` on text and numbers; `int(...)` to convert text; `ValueError` and `TypeError`; money in whole cents.
- 13.4: `if` / `else`, `==` and comparisons, indentation blocks, `for` loops over a list, filtering inside a loop, a one-line list comprehension filter.
- 13.5: `and`, `or`, `not`; empty values (`""`, `None`, `0`) and the `0` trap; `while` loops and the line that changes their condition.
- 13.6: `def`, parameters with type labels, return types (`-> int`, `-> str`), `return`, pure functions, `assert` with a message.
- 13.7: lists and dictionaries (`dict[str, str]`), keys and values, records, `KeyError`, `.get(key, default)`, `IndexError`, `sorted()` with `key=` and `reverse=True`, CSV rows as records.

Not covered yet (each needs teaching before use): reading files (13.8), dates (13.9), reading errors and `try` / `except` (13.10), tests-first with named test functions and pytest (13.11), `import` of modules and the standard library, `-> None`, `break` / `continue`, default parameter values, docstrings, classes and objects (Chapter 14), dataclasses.

### Rules

- Use only the concepts listed above, so the user can read every line.
- Before using any new concept, teach it first with **PRIMM-AI+**, the course's method, and only use it in Mailroom once the user has worked through it:
  1. **Predict**: show a small example and ask the user what it will do. Don't run it yet, and don't hint.
  2. **Run**: run it (with permission) and show the real output.
  3. **Investigate**: compare the prediction with the output; explain a line when the user asks why.
  4. **Modify**: the user changes one thing, predicts again, runs again; make the edit they describe.
  5. **Make**: the user specifies their own version; write code against that spec, and the user checks it with a run or a test.
- Predict before you run, every time. A run or a test decides.
- On every change, run the tests, the type checker in strict mode, and any linter the project has.

## Commands

The project uses [uv](https://docs.astral.sh/uv/) and Python 3.14 (pinned in `.python-version`). Always go through `uv run` rather than calling `python` or `pytest` directly.

```bash
uv sync                                   # create .venv and install dependencies
uv run mailroom                           # run the CLI (entry point: mailroom:main)
uv run pytest                             # run all tests
uv run pytest tests/test_main.py::test_main_prints_greeting   # run one test
uv add <pkg>                              # add a runtime dependency
uv add --dev <pkg>                        # add a dev-only dependency
```

No linter or formatter is configured yet.

## Layout

- `src/mailroom/` is the package (src layout, built with `uv_build`). The `mailroom` console script in `pyproject.toml` points at `mailroom:main` in `__init__.py`.
- `tests/` holds pytest tests. pytest is the only dev dependency.
- `uv.lock` is committed; update it through `uv add` / `uv sync`, not by hand.
- `.venv` is not shared between machines; run `uv sync` to create it.

## Where the code lives

- The user's laptop (Windows): `D:\Claude\FDE102\mailroom`, next to `D:\Claude\FDE102\my-email-studio` (the Email Studio for step 4).
- There is no Git repository yet.
