# Makefile for globomap-driver-napi

# Version package
VERSION=$(shell python -c 'import globomap_driver_napi; print(globomap_driver_napi.__version__)')

# PIP
PIP := $(shell which pip)

help:
	@echo
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  clean      to clean garbage left by builds and installation"
	@echo "  dist       to create egg for distribution"
	@echo "  publish    to publish the package to PyPI"
	@echo "  setup      to install requirements"
	@echo "  test       to execute all tests"
	@echo

clean:
	@rm -rf build dist *.egg-info
	@find . \( -name '*.pyc' -o  -name '__pycache__' -o -name '**/*.pyc' -o -name '*~' \) -delete

dist: clean
	@python setup.py sdist

publish: clean dist
	@echo 'Ready to release version ${VERSION}? (ctrl+c to abort)' && read
	twine upload dist/*
	@git tag ${VERSION}
	@git push --tags

setup: requirements_test.txt
	$(PIP) install -r $^

test:
	@nosetests --verbose --rednose  --nocapture --cover-package=globomap_driver_napi; coverage report -m
