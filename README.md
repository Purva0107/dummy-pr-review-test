# dummy-pr-review-test

Minimal Python repo for manually testing the [PR Review Agent](https://github.com/Purva0107/dummy-pr-review-test) pipeline.

- **`main`** — clean baseline with passing pytest tests
- **Feature branches** — intentional low / medium / high / critical bugs

See [TEST_PR_GUIDE.md](TEST_PR_GUIDE.md) for the full branch → severity mapping.

```bash
pip install -r requirements.txt
pytest -q
```
