all: lint coverage

test:
	python -m pytest -vv

lint:
	python -m ruff check $(if $(GITHUB_ACTIONS),--format github,) .

format:
	python -m ruff check --fix .

coverage:
	python -m pytest -q --cov=prfiesta --cov-report=term # for local
	python -m pytest -q --cov=prfiesta --cov-report=html # for local
	python -m pytest -q --cov=prfiesta --cov-report=xml  # for sonarqube

export_requirements:
	poetry export --with dev --output requirements.txt

clean:
	rm ./coverage.xml
	rm -rf ./htmlcov
	rm -rf ./.pytest_cache
	rm -rf ./.ruff_cache
