# PR Review Agent — Test Harness Guide

This repo contains intentional bugs on feature branches for end-to-end testing of the PR Review Agent.

## Baseline (`main`)

Clean code + pytest suite. All tests pass on `main`.

## Open test PRs

| Branch | Severity | Bug planted | Category | Sandbox / static |
|---|---|---|---|---|
| `test/low-style-only` | **low** | Unused import, f-string without placeholders, dead variable | style | ruff |
| `test/high-div-by-zero` | **high** | `get_average([])` → ZeroDivisionError | logic | **pytest fails** |
| `fix/low-average-bug` | **high** | Same as above (legacy branch name) | logic | **pytest fails** |
| `test/medium-user-age-keyerror` | **medium** | `get_user_age` KeyError on missing key | logic | **pytest fails** |
| `fix/medium-user-age-bug` | **medium** | Same as above (legacy branch) | logic | **pytest fails** |
| `test/medium-race-counter` | **medium** | Non-atomic counter increment | race_condition | flaky pytest |
| `test/critical-security` | **critical** | SQL string concat + hardcoded secret | security | semgrep |
| `fix/critical-sql-injection` | **critical** | Same as above (legacy branch) | security | semgrep |
| `test/mixed-all-severities` | **mixed** | Style + logic + race + security together | multiple | partial |
| `chore/test-harness` | none | Adds pytest + docs only | — | all pass |

## How to trigger a review

1. Point your webhook at this repo (`Purva0107/dummy-pr-review-test`).
2. Open or synchronize a PR from one of the branches above.
3. Compare agent findings against the table.

## Re-run a review

Push an empty commit to the PR branch or close/reopen the PR to fire `pull_request` `synchronize` / `opened` events.
