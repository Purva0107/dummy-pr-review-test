# PR Review Agent — Test Harness Guide

This repo contains intentional bugs on feature branches for end-to-end testing of the PR Review Agent.

## Baseline (`main`)

Clean code + pytest suite. All tests pass on `main`.

## Open test PRs

| PR branch | Target severity | Bug planted | Expected category | Sandbox confirms? |
|---|---|---|---|---|
| `test/low-style-only` | **low** | Unused import, f-string without placeholders | style | no (ruff/static) |
| `fix/low-average-bug` | **high** | `get_average([])` → ZeroDivisionError | logic | **yes** (pytest fails) |
| `fix/medium-user-age-bug` | **medium** | `get_user_age` KeyError on missing key | logic | **yes** (pytest fails) |
| `test/medium-race-counter` | **medium** | Non-atomic counter increment | race_condition | no (needs threaded test) |
| `fix/critical-sql-injection` | **critical** | SQL string concat + hardcoded secret | security | semgrep |
| `test/mixed-all-severities` | mixed | Style + logic + security in one PR | multiple | partial |

## How to trigger a review

1. Point your webhook at this repo (`Purva0107/dummy-pr-review-test`).
2. Open or synchronize a PR from one of the branches above.
3. Compare agent findings against the table.

## Re-run a review

Push an empty commit to the PR branch or close/reopen the PR to fire `pull_request` `synchronize` / `opened` events.
