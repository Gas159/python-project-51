install:
	poetry install
install1:
	poetry install
	poetry build
build:
	poetry build
publish:
	poetry publish --dry-run
patch:
	python3 -m pip inmake stall --user --force-reinstall dist/*.whl
patch1:
	python3 -m pip install --user dist/*.whl
lint:
	poetry run flake8 page_loader
lint1:
	poetry run flake8 tests
test:
	poetry run pytest -vv
#	poetry run flake8 page_loader
test_cov:
	poetry run pytest --cov=page_loader tests/ --cov-report xml
test1_cov:
	poetry run pytest --cov=page_loader



fast-check: # -s print -v\-vv verbose op1
	poetry install
	poetry build
	python3 -m pip install --user --force-reinstall dist/*.whl
	poetry run flake8 page_loader
	poetry run pytest -vv
	poetry run pytest --cov=page_loader

check-in:
	echo "\n\n ! Build process...\n"
	make build
	echo "\n\n\n ! Package-force-reinstall process...\n"
	make patch
	echo "\n\n\n ! Lint checkup process...\n"
	make lint
	echo "\n\n\n ! Test checkup process...\n"
	make test
