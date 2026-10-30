# Change Machine — common tasks. Run `make` (or `make help`) to list them.

PYTHON  ?= python3
VENV    ?= .venv
BIN     := $(VENV)/bin
IMAGE   ?= change-machine
TAG     ?= latest
PORT    ?= 5000

.DEFAULT_GOAL := help

.PHONY: help
help: ## Show this help
	@grep -hE '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

# ── Local ─────────────────────────────────────────────────────────────────────

$(BIN)/activate: pyproject.toml
	$(PYTHON) -m venv $(VENV)
	$(BIN)/pip install --upgrade pip
	$(BIN)/pip install -e ".[dev]"
	@touch $@

.PHONY: install
install: $(BIN)/activate ## Create .venv and install the app + dev tools

.PHONY: run
run: install ## Run the dev server with live reload (default http://localhost:5000)
	$(BIN)/flask --app sample_1.app run --debug --port $(PORT)

.PHONY: lint
lint: install ## Lint with ruff
	$(BIN)/ruff check .

.PHONY: fmt
fmt: install ## Auto-fix lint issues and format code
	$(BIN)/ruff check --fix .
	$(BIN)/ruff format .

.PHONY: typecheck
typecheck: install ## Type-check with mypy
	$(BIN)/mypy sample_1

.PHONY: test
test: install ## Run tests with coverage
	$(BIN)/pytest -v

.PHONY: check
check: lint typecheck test ## Lint + typecheck + tests (same as CI)

.PHONY: lock
lock: ## Regenerate requirements.txt (pinned runtime deps for Docker)
	rm -rf .lockenv && $(PYTHON) -m venv .lockenv
	.lockenv/bin/pip install -q .
	{ echo "# Pinned runtime dependencies for the Docker image (tested versions)."; \
	  echo "# Regenerate with: make lock"; \
	  .lockenv/bin/pip freeze --exclude-editable | grep -vi '^sample.code.1'; } > requirements.txt
	rm -rf .lockenv build

# ── Docker ────────────────────────────────────────────────────────────────────

.PHONY: docker-build
docker-build: ## Build the production image
	docker build -f Dockerfile-prod -t $(IMAGE):$(TAG) .

.PHONY: docker-run
docker-run: docker-build ## Run the production image (default http://localhost:5000)
	docker run --rm -p $(PORT):5000 --read-only --tmpfs /tmp $(IMAGE):$(TAG)

.PHONY: docker-dev
docker-dev: ## Run the dev container with live reload (docker compose)
	HOST_PORT=$(PORT) docker compose --profile dev up --build

.PHONY: docker-test
docker-test: ## Run lint + typecheck + tests inside the dev image
	docker compose --profile dev build web-dev
	docker compose --profile dev run --rm --no-deps web-dev sh -c "ruff check . && mypy sample_1 && pytest -v"

.PHONY: up
up: ## Start the production stack in the background (docker compose)
	HOST_PORT=$(PORT) docker compose --profile prod up -d --build

.PHONY: down
down: ## Stop all compose services
	docker compose --profile dev --profile prod down

# ── Housekeeping ──────────────────────────────────────────────────────────────

.PHONY: clean
clean: ## Remove caches, build output, and .venv
	rm -rf $(VENV) build dist *.egg-info .pytest_cache .mypy_cache .ruff_cache .coverage htmlcov
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
