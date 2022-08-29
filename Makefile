install:
	poetry install

build:
	poetry build

package-install:
	python3 -m pip install --user dist/*.whl

lint:
	poetry run flake8 sentry

black:
	poetry run black sentry

isort:
	poetry run isort sentry

test:
	poetry run pytest --cov=sentry --cov-report xml tests/

mypy:
	poetry run mypy --strict sentry/

.PHONY: install build package-install lint isort black test mypy
