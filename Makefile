fmt:
	@pipenv run black .

pep8:
	@pipenv run flake8 .

install-dev:
	@pipenv install --dev

install:
	@pipenv install
