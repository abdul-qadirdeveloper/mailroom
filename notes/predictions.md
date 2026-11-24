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

### Two problems at once

One check runs all five rules and returns every problem it finds, in rule order.

| # | Issue | What the check should say |
|---|-------|---------------------------|
| 1 | issue-01, but the subject is `Your 10-minute walk plan is ready, starting today!!` (51) and the `Unsubscribe:` part is removed | `["Problem: subject is 51 characters, the limit is 50", "Problem: no Unsubscribe line"]` |
