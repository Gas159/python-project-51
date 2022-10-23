build:
    poetry build
install:
    poetry install
patch:
	python3 -m pip install --user --force-reinstall dist/*.whl