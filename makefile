all: lint coverage

test:
	python -m pytest -vv

lint:
	python -m ruff check .

format:
	python -m ruff check --fix .

coverage:
	python -m pytest --cov=prfiesta --cov-report=term # for local
	python -m pytest --cov=prfiesta --cov-report=html # for local
	python -m pytest --cov=prfiesta --cov-report=xml  # for sonarqube

clean:
	rm ./coverage.xml
	rm -rf ./htmlcov
	rm -rf ./.pytest_cache
	rm -rf ./.ruff_cache
