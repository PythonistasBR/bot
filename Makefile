.PHONY: help

help:
	@echo "Usage: make command"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

run: update_webhook ## Run bot using flask as server
	@pipenv run flask run --host 0.0.0.0

test: ## Run pytest
	@pipenv run pytest --cov=autonomia tests/

coverage: ## Run test and create HTML coverage report
	@pipenv run py.test --cov=autonomia --cov-report html tests/

fmt: ## Format code using iSort and Black
	@pipenv run isort .
	@pipenv run black .

lint: ## Run flake8
	@pipenv run flake8 .
	@pipenv run black --check .
	@pipenv run isort --check-only .

update_webhook: ## Update telegram webhook config from settings
	@pipenv run flask update_webhook

heroku_update_webhook:
	heroku run FLASK_APP=autonomia/app.py flask update_webhook

install-dev: ## Install all dependencies
	@pipenv install --dev

install: ## Install only prod dependencies
	@pipenv install

clean: ## Clean all compiled python code
	@find . -name __pycache__ -delete -or -iname "*.py[co]" -delete

# docker commands
start: up  ## [docker] - start bot
	@sudo docker-compose start

stop: ## [docker] - Stop bot
	@sudo docker-compose stop

up:
	@sudo docker-compose up -d

rebuild: down  ## [docker] - rebuild bot
	@sudo docker-compose rm
	@sudo docker-compose build

down:
	@sudo docker-compose down

logs:  ## [docker] - tail bot logs
	@sudo docker-compose logs --tail 60 -f

restart: stop start

kill:
	@sudo docker-compose kill

status:  ## [docker] - check bot status
	@sudo docker-compose ps

docker-update-webhook:  ## [docker] - update telegram webhook config from settings
	@sudo docker-compose run --no-deps --rm web flask update_webhook
