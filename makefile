install:
	poetry build
	poetry install
	poetry build
build:
	poetry build
publish:
	poetry publish --dry-run
patch:
	python3 -m pip install --user --force-reinstall dist/*.whl
patch1:
	python3 -m pip install --user dist/*.whl
lint:
	poetry run flake8 page_loader
lint1:
	poetry run flake8 tests
test:
	poetry run pytest -vv
	poetry run flake8 page_loader
test_cov:
	poetry run pytest --cov=page_loader tests/ --cov-report xml
test1_cov:
	poetry run pytest --cov=page_loader