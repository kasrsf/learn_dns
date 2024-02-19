.PHONY: init test lint run


init:
	@echo "Checking for Poetry..."
	@command -v poetry >/dev/null 2>&1 || { echo >&2 "Installing Poetry..."; \
	curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -; }
	@echo "Poetry is installed."
	@echo "Initializing virtual environment..."
	@poetry install

test:
	poetry run pytest

lint:
	poetry run ruff check .

format:
	poetry run ruff format .
