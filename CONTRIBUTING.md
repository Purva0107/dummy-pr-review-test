# Contributing

1. Branch from `main` (`feature/<ticket>-short-name`).
2. Keep PRs focused; include tests for behavior changes.
3. Run `pytest -q` before opening a PR.
4. Do not commit secrets; use `.env` locally (never push).

## Code style

- Prefer explicit types on public service functions.
- Money values are integer **cents**.
- DB access goes through repositories, not routers.
