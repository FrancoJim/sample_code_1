# Change Machine

A Flask web app and JSON REST API that returns the optimal (fewest pieces) USD coin and bill breakdown for any dollar amount.

## Denominations

| Bill / Coin      | Value  |
|------------------|--------|
| Hundred Dollar Bill | $100.00 |
| Fifty Dollar Bill   | $50.00  |
| Twenty Dollar Bill  | $20.00  |
| Ten Dollar Bill     | $10.00  |
| Five Dollar Bill    | $5.00   |
| Two Dollar Bill     | $2.00   |
| One Dollar Bill     | $1.00   |
| Half Dollar         | $0.50   |
| Quarter             | $0.25   |
| Dime                | $0.10   |
| Nickel              | $0.05   |
| Penny               | $0.01   |

---

## REST API

```
GET /api/v1/change?amount=<value>
```

**Example:**
```bash
curl "http://localhost:5000/api/v1/change?amount=1.23"
```

```json
{
  "total": "1.23",
  "change": [
    {"denom_name": "One Dollar Bill", "count": 1, "denom_amount": "1.00"},
    {"denom_name": "Dime",            "count": 2, "denom_amount": "0.10"},
    {"denom_name": "Penny",           "count": 3, "denom_amount": "0.01"}
  ]
}
```

| Status | Condition |
|--------|-----------|
| `200`  | Valid amount |
| `400`  | Missing, non-numeric, or non-positive amount |

---

## Development

### Option A — Dev Container (recommended)

Requires [Cursor](https://cursor.sh) or VS Code with the
[Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension, plus [OrbStack](https://orbstack.dev) or Docker Desktop.

1. Open the repo root in Cursor / VS Code.
2. When prompted, click **Reopen in Container** — or run  
   `Dev Containers: Reopen in Container` from the command palette.
3. The container builds once, then `postCreateCommand` installs the project and dev tools automatically.

Inside the container a custom prompt shows your git context:

```
sample_code_1 | master | ~/workspace/sample_code_1 $
```

Useful shell shortcuts pre-loaded:

| Alias       | Command                               |
|-------------|---------------------------------------|
| `serve`     | `flask run` (binds `0.0.0.0:5000`)   |
| `run-tests` | `pytest -v`                           |
| `lint`      | `ruff check .`                        |
| `typecheck` | `mypy sample_1`                       |
| `check`     | lint + typecheck + tests in sequence  |
| `dc`        | `docker compose`                      |

### Option B — Local virtualenv

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
flask --app sample_1.app run --debug
```

---

## Docker Deployment

Copy the env file first:

```bash
cp example.env .env
```

**Development** (live-reload, mounts source):
```bash
docker compose --profile dev up --build
```

**Production** (multi-stage build, gunicorn, non-root user):
```bash
docker compose --profile prod up -d --build
```

Browse to `http://localhost:5000`.

---

## Tests

```bash
pytest -v
```

The suite covers denomination correctness, edge cases (zero, negative), and the classic float-precision trap (`1.15 * 100 = 114.999…` in float arithmetic — handled with `Decimal` throughout).

---

## CI

GitHub Actions runs on every push and pull request to `master`:

1. **test** — ruff lint → mypy type-check → pytest
2. **docker** — builds the production image (only runs if tests pass)

---

## Contributing

Contributions are accepted in forms of employment or large sums of money.

## License

[MIT](https://choosealicense.com/licenses/mit/)
