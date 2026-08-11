# Webhook setup for PR Review Agent

Point a GitHub repo webhook at your local tunnel (same as the dummy harness).

## Settings

| Field | Value |
|---|---|
| Payload URL | `https://<your-tunnel>.trycloudflare.com/webhook` |
| Content type | `application/json` |
| Secret | Same as `GITHUB_WEBHOOK_SECRET` in the agent `.env` |
| Events | **Pull requests** + **Pull request review comments** |

## Allowlist

Ensure the agent `.env` includes:

```env
REPO_ALLOWLIST=Purva0107/dummy-pr-review-test,Purva0107/acme-orders-api
```

Then restart the API and worker.
