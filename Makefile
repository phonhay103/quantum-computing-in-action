.PHONY: help install sync lint format test clean ch01 ch02 ch03 ch04 ch05 docs docs-serve

# Default target
.DEFAULT_GOAL := help

help: ## Display available commands
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

install: sync ## Alias for sync

sync: ## Install dependencies from uv.lock
	uv sync

lint: ## Run lint checks with Ruff and ty
	uv run ruff check .
	uv run ty check

format: ## Format code with Ruff
	uv run ruff format .

test: ## Run the test suite with pytest
	uv run pytest tests/

ch01: ## Run chapter 1 (factoring time complexity)
	uv run python -m quantum_computing_in_action ch01

ch02: ## Run chapter 2 (random bits)
	uv run python -m quantum_computing_in_action ch02

ch03: ## Run chapter 3 (Pauli-X gate)
	uv run python -m quantum_computing_in_action ch03

ch04: ## Run chapter 4 (Hadamard gate)
	uv run python -m quantum_computing_in_action ch04

ch05: ## Run chapter 5 (entanglement)
	uv run python -m quantum_computing_in_action ch05

assets: ## Copy generated diagrams into the docs tree
	@mkdir -p docs/assets
	@cp build/*.png docs/assets/

docs: assets ## Build the documentation site into site/
	uv run mkdocs build --strict

docs-serve: assets ## Serve the documentation site locally
	uv run mkdocs serve

clean: ## Remove caches and build artifacts
	rm -rf .pytest_cache .ruff_cache .ty dist build site docs/assets
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
