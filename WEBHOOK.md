# Webhook setup for PR Review Agent (Acme Orders harness)

## Where the code lives

The PAT could not create a standalone `Purva0107/acme-orders-api` repo (`403 Resource not accessible by personal access token`). The clean Acme tree was therefore published as an **orphan branch** on the existing harness repo:

| Item | Value |
|---|---|
| Repo | `Purva0107/dummy-pr-review-test` (webhook already configured) |
| Clean base | branch `acme-main` |
| Bug PRs | #16–#20 against `acme-main` |

If you later create `Purva0107/acme-orders-api`, push `acme-main` there as `main`, re-open the five PRs, add the same webhook, and extend `REPO_ALLOWLIST`.

## Webhook (same as dummy)

| Field | Value |
|---|---|
| Payload URL | `https://<your-tunnel>.trycloudflare.com/webhook` |
| Content type | `application/json` |
| Secret | Same as `GITHUB_WEBHOOK_SECRET` in the agent `.env` |
| Events | **Pull requests** + **Pull request review comments** |

No new webhook is required while testing on `dummy-pr-review-test` / `acme-main`.

## Allowlist

```env
REPO_ALLOWLIST=Purva0107/dummy-pr-review-test,Purva0107/acme-orders-api
```

`dummy-pr-review-test` is required for the current orphan-branch setup. Restart the API and worker after changing allowlist.
