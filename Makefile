.PHONY: help install sync lint format test clean

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

clean: ## Remove caches and build artifacts
	rm -rf .pytest_cache .ruff_cache .ty dist build
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
