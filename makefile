all: lint coverage

sync:
	uv sync --locked

build:
	uv build

test:
	uv run pytest -vv

lint:
	uv run ruff check $(if $(GITHUB_ACTIONS),--output-format github,) .

format:
	uv run ruff format .
	uv run ruff check --fix .

coverage:
	uv run pytest -q --cov=prfiesta --cov-report=term # for local
	uv run pytest -q --cov=prfiesta --cov-report=html # for local

coverage_ci:
	uv run pytest -q --cov=prfiesta --cov-report=xml --cov-report=lcov

precommit_install:
	uv run pre-commit install

precommit_run:
	uv run pre-commit run --all-files

validate_notebooks:
	uv run bash ./notebooks/scripts/run_all.sh './notebooks/plots/*.ipynb' 'notebooks/plots'
	uv run bash ./notebooks/scripts/run_all.sh './notebooks/views/*.ipynb' 'notebooks/views'

integration_test:
	uv run papermill --cwd notebooks/misc ./notebooks/misc/integration_test.ipynb ./notebooks/misc/integration_test.ipynb

clean:
	rm -rf ./htmlcov
	rm -rf ./.pytest_cache
	rm -rf ./.ruff_cache

local_cross_version_sanity_check:
	uvx --python 3.10 --prerelease allow prfiesta -u kiran94 --after 2025-01-01
	uvx --python 3.11 --prerelease allow prfiesta -u kiran94 --after 2025-01-01
	uvx --python 3.12 --prerelease allow prfiesta -u kiran94 --after 2025-01-01
	uvx --python 3.13 --prerelease allow prfiesta -u kiran94 --after 2025-01-01
	uvx --python 3.14 --prerelease allow prfiesta -u kiran94 --after 2025-01-01
