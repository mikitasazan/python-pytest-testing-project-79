install:
	uv sync

build:
	uv build

package-install:
	uv tool install dist/*.whl

page-loader:
	uv run page-loader

lint:
	uv run ruff check page_loader tests

test:
	uv run pytest

test-coverage:
	uv run pytest --cov=page_loader --cov-report xml --cov-report term
