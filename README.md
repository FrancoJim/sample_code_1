# Change Machine

[![CI](https://github.com/FrancoJim/sample_code_1/actions/workflows/ci.yml/badge.svg)](https://github.com/FrancoJim/sample_code_1/actions/workflows/ci.yml)

A Flask web app and JSON REST API that returns the optimal (fewest pieces) USD coin and bill breakdown for any dollar amount.

## Highlights

- **Exact money math** with `Decimal` end to end (input strings never pass through `float`)
- **Input hardening**: `nan`, `inf`, huge or junk amounts return a clean `400`, never a `500`
- **100% test coverage** across the core logic, the web form, and the JSON API
- **Production container**: multi-stage build, pinned deps, non-root user, read-only filesystem, built-in health check
- **CI** on Python 3.11–3.14, plus a Docker build and smoke test; Dependabot keeps deps current
- **One-command workflow** with `make`

## Quick start

```bash
make            # list every task
make check      # create .venv, then lint + typecheck + tests
make run        # dev server at http://localhost:5000
make docker-run # build and run the production image
```

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
  "change": [
    {"count": 1, "denom_amount": "1.00", "denom_name": "One Dollar Bill"},
    {"count": 2, "denom_amount": "0.10", "denom_name": "Dime"},
    {"count": 3, "denom_amount": "0.01", "denom_name": "Penny"}
  ],
  "total": "1.23"
}
```

| Status | Condition |
|--------|-----------|
| `200`  | Valid amount |
| `400`  | Missing, non-numeric, non-finite (`nan`, `inf`), non-positive, or over $1,000,000,000 |

Amounts are rounded to the nearest cent (half up), so `0.005` becomes `0.01`.

```
GET /healthz   →  {"status": "ok"}
```

Used by the Docker `HEALTHCHECK` and the CI smoke test.

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

### Option B — Local virtualenv (Makefile)

Requires Python 3.11+.

```bash
make install   # creates .venv and installs the app + dev tools
make run       # flask dev server with live reload
make check     # ruff + mypy + pytest
```

Or by hand:

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
make docker-dev        # or: docker compose --profile dev up --build
make docker-test       # run lint + typecheck + tests inside the container
```

**Production** (multi-stage build, pinned deps, gunicorn, non-root, read-only, health check):
```bash
make up                # or: docker compose --profile prod up -d --build
make down
```

Browse to `http://localhost:5000`. Port 5000 is taken on many Macs (AirPlay Receiver); use another with `make run PORT=5050`, `make up PORT=5050`, etc.

`requirements.txt` pins the exact runtime versions the production image installs. Regenerate it after changing dependencies with `make lock`.

---

## Tests

```bash
make test   # or: pytest -v
```

Coverage is reported on every run. The suite covers the web form, the JSON API (including `400` handling), the health check, denomination correctness, edge cases (zero, negative), and the classic float-precision trap (`1.15 * 100 = 114.999…` in float arithmetic — handled with `Decimal` throughout).

---

## CI

GitHub Actions runs on every push and pull request to `master`:

1. **test** — ruff lint → mypy type-check → pytest, on Python 3.11, 3.12, 3.13 and 3.14
2. **docker** — builds the production image, starts it, and smoke-tests `/healthz` and the API (only runs if tests pass)

Dependabot opens weekly update PRs for Python packages, GitHub Actions, and the Docker base image.

---

## Contributing

Contributions are accepted in forms of employment or large sums of money.

## License

[MIT](https://choosealicense.com/licenses/mit/)
