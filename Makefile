# Makefile for globomap-driver-napi

# Version package
VERSION=$(shell python -c 'import globomap_driver_napi; print globomap_driver_napi.VERSION')

# Pip executable path
PIP := $(shell which pip)

# GloboNetworkAPI project URL
GLNAPIURL := https://github.com/globocom/globomap-driver-napi.git

help:
	@echo
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  docs       to create documentation files"
	@echo "  clean      to clean garbage left by builds and installation"
	@echo "  compile    to compile .py files (just to check for syntax errors)"
	@echo "  test       to execute all tests"
	@echo "  build      to build without installing"
	@echo "  install    to install"
	@echo "  dist       to create egg for distribution"
	@echo "  publish    to publish the package to PyPI"
	@echo "  setup      to setup environment locally to run project"
	@echo "  test_setup to setup test environment locally to run tests"
	@echo

clean:
	@echo "Cleaning project ..."
	@rm -rf build dist *.egg-info
	@find . \( -name '*.pyc' -o -name '**/*.pyc' -o -name '*~' \) -delete

compile: clean
	@echo "Compiling source code..."
	@python -tt -m compileall .
	@pep8 --format=pylint --statistics globomap_driver_napi setup.py

setup: requirements.txt
	$(PIP) install -r $^

install:
	@python setup.py install

dist: clean
	@python setup.py sdist

publish: clean dist
	@echo 'Ready to release version ${VERSION}? (ctrl+c to abort)' && read
	twine upload dist/*
	@git tag ${VERSION}
	@git push --tags

