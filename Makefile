# version
NAME?=$(shell awk -F\" '/^name *=/ { print $$2; exit; }' pyproject.toml)
VERSION?=$(shell awk -F\" '/^version *=/ { print $$2; exit; }' pyproject.toml)

# poetry (in-project virtual env name is `.venv`)
POETRY:=$(shell command -v poetry 2> /dev/null)
POERTY_RUN:=$(POETRY) run
POETRY_LOCK:=poetry.lock
POETRY_VENV:=.venv
POETRY_VENV_STAMP:=$(POETRY_VENV)/.install.stamp

# tests
SRC_DIR?=aoc2022

.PHONY: help
help: ## This help message
	@grep -E '^[a-zA-Z/_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sed 's/.*Makefile[^:]*://g' | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

$(POETRY_LOCK):
	@$(POETRY) install

$(POETRY_VENV_STAMP): pyproject.toml $(POETRY_LOCK)
	@if [ -z $(POETRY) ]; then echo Poetry could not be found. See https://python-poetry.org/docs/; exit 2; fi
	@$(POETRY) update && touch $(POETRY_VENV_STAMP)

.PHONY: venv/create
venv/create: $(POETRY_VENV_STAMP) ## setup the python virtual environment

.PHONY: venv/clean
venv/clean: ## clean the python virtual environment
	@rm -rf $(POETRY_VENV)

.PHONY: setup
setup: venv/create ## setup the dev environment

.PHONY: clean
clean: venv/clean ## clean the dev environment, caches and the doc
	@rm -rf .mypy_cache .pytest_cache **/__pycache__

.PHONY: lint/style
lint/style: venv/create ## run formatting linters (on the app and tests)
	@$(POERTY_RUN) isort --check-only $(SRC_DIR) && \
		$(POERTY_RUN) flake8 $(SRC_DIR)

.PHONY: lint/type
lint/type: venv/create ## run the static type checking (only on the app)
	@$(POERTY_RUN) mypy $(SRC_DIR) --strict

.PHONY: lint
lint: lint/style lint/type ## run linting

.PHONY: lint/fix
lint/fix: venv/create ## run linting and fix issues
	@$(POERTY_RUN) yapf --recursive --in-place $(SRC_DIR) && \
		$(POERTY_RUN) isort $(SRC_DIR) && \
		$(POERTY_RUN) autoflake8 --recursive --in-place --remove-unused-variables $(SRC_DIR)

.PHONY: create
create: ## Scaffold and download input for the specified DAY
	@poetry run aoc create $(DAY)

.PHONY: run
run: ## Run the code of the specified DAY
	@poetry run aoc run $(DAY)

.PHONY: watch
watch: ## Watch for changes in the code of the specified DAY and run it
	@poetry run when-changed -v -r -1 aoc2022/day$$(printf "%02d" $(DAY))/*.py aoc run $(DAY)
