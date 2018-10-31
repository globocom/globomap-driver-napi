# Makefile for globomap-driver-napi

# Version package
VERSION=$(shell python -c 'import globomap_driver_napi; print(globomap_driver_napi.__version__)')

# PIP
PIP := $(shell which pip)

help:
	@echo
	@echo "Please use 'make <target>' where <target> is one of"
	@echo

	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

clean: ## Clear *.pyc files, etc
	@rm -rf build dist *.egg-info
	@find . \( -name '*.pyc' -o  -name '__pycache__' -o -name '**/*.pyc' -o -name '*~' \) -delete

dist: clean ## Create egg for distribution
	@python setup.py sdist

publish: clean dist ## Publish the package to PyPI
	@echo 'Ready to release version ${VERSION}? (ctrl+c to abort)' && read
	twine upload dist/*
	@git tag ${VERSION}
	@git push --tags

setup: requirements_test.txt ## Install project dependencies
	$(PIP) install -r $^

tests: clean ## Make tests
	@nosetests --verbose --rednose  --nocapture --cover-package=globomap_driver_napi --with-cover; coverage report -m

tests_ci: clean ## Make tests to CI
	@nosetests --verbose --rednose  --nocapture --cover-package=globomap_driver_napi

run_loader: ## Run Full loader
	@PYTHONPATH=`pwd`:$PYTHONPATH python globomap_driver_napi/run_loader.py

run_consumer: ## Run consumer
	@PYTHONPATH=`pwd`:$PYTHONPATH python globomap_driver_napi/consumer.py

run_scheduler: ## Run scheduler
	@PYTHONPATH=`pwd`:$PYTHONPATH python globomap_driver_napi/scheduler.py
