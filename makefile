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

	# for sonarqube
	$(if $(GITHUB_ACTIONS),python -m pytest -q --cov=prfiesta --cov-report=xml,)

	# for github action
	$(if $(GITHUB_ACTIONS),python -m pytest -q --cov=prfiesta --cov-report=lcov,)

export_requirements:
	poetry export --with dev --output requirements.txt

precommit_install:
	pre-commit install

precommit_run:
	pre-commit run --all-files

validate_notebooks:
	cd ./notebooks/plots/ && ./run_all.sh
	cd ./notebooks/views/ && ./run_all.sh

clean:
	rm ./coverage.xml
	rm -rf ./htmlcov
	rm -rf ./.pytest_cache
	rm -rf ./.ruff_cache
