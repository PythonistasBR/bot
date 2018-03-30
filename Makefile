help:
	@echo "Usage: make command"
	@echo "run           - Run autonomia bot"
	@echo "fmt           - Format code using Black"
	@echo "lint          - Run flake8"
	@echo "install-dev   - Install all dependencies"
	@echo "install       - Install only prod dependencies"
	@echo "clean         - Clean all compiled python code"

run:
	@pipenv run python autonomia.py

fmt:
	@pipenv run black .

lint:
	@pipenv run flake8 .

install-dev:
	@pipenv install --dev

install:
	@pipenv install

clean:
	@find . -name __pycache__ -delete -or -iname "*.py[co]" -delete
