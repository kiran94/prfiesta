test:
	python -m pytest

lint:
	python -m ruff check .

format:
	python -m ruff check --fix .

coverage:
	python -m pytest --cov=prfiesta --cov-report=term # for local
	python -m pytest --cov=prfiesta --cov-report=html # for local
	python -m pytest --cov=prfiesta --cov-report=xml  # for sonarqube
