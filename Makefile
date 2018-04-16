.PHONY: help

help:
	@echo "Usage: make command"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

run: ## Run autonomia bot
	@pipenv run python -m autonomia

run_flask: ## Run bot using flask as server
	@pipenv run flask run

test: ## Run pytest
	@pipenv run pytest --cov=autonomia tests/

coverage: ## Run test and create HTML coverage report
	@pipenv run py.test --cov=autonomia --cov-report html tests/

fmt: ## Format code using iSort and Black
	@pipenv run isort -rc --atomic .
	@pipenv run black .

lint: ## Run flake8
	@pipenv run flake8 .

install-dev: ## Install all dependencies
	@pipenv install --dev

install: ## Install only prod dependencies
	@pipenv install

clean: ## Clean all compiled python code
	@find . -name __pycache__ -delete -or -iname "*.py[co]" -delete
