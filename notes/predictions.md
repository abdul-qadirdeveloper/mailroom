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
