all: lint coverage

test:
	poetry run pytest -vv

lint:
	poetry run ruff check $(if $(GITHUB_ACTIONS),--output-format github,) .

format:
	poetry run ruff format .
	poetry run ruff check --fix .

coverage:
	poetry run pytest -q --cov=prfiesta --cov-report=term # for local
	poetry run pytest -q --cov=prfiesta --cov-report=html # for local

	# for sonarqube
	$(if $(GITHUB_ACTIONS),poetry run pytest -q --cov=prfiesta --cov-report=xml,)

	# for github action
	$(if $(GITHUB_ACTIONS),poetry run pytest -q --cov=prfiesta --cov-report=lcov,)

export_requirements:
	poetry export --with dev --output requirements.txt

precommit_install:
	pre-commit install

precommit_run:
	pre-commit run --all-files

validate_notebooks:
	poetry run bash ./notebooks/scripts/run_all.sh './notebooks/plots/*.ipynb' 'notebooks/plots'
	poetry run bash ./notebooks/scripts/run_all.sh './notebooks/views/*.ipynb' 'notebooks/views'

integration_test:
	poetry run papermill --log-output --cwd notebooks/misc ./notebooks/misc/integration_test.ipynb ./notebooks/misc/integration_test.ipynb

clean:
	rm -rf ./htmlcov
	rm -rf ./.pytest_cache
	rm -rf ./.ruff_cache
