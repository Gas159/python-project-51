install:
	poetry install
build:
	poetry build
publish:
	poetry publish --dry-run
patch:
	python3 -m pip install --user --force-reinstall dist/*.whl
patch1:
	python3 -m pip install --user dist/*.whl
lint:
	poetry run flake8 gendiff
lint1:
	poetry run flake8 tests
test:
	poetry run pytest -vv
#poetry run flake8 page_loader
test_cov:
	poetry run pytest --cov=gendiff tests/ --cov-report xml
test1_cov:
	poetry run pytest --cov=gendiff