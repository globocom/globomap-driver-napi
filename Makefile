# Makefile for globomap-driver-napi

# Version package
VERSION=$(shell python -c 'import globomap_driver_napi; print(globomap_driver_napi.__version__)')

help:
	@echo
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  clean      to clean garbage left by builds and installation"
	@echo "  deploy     to deploy project in Tsuru"
	@echo "  test       to execute all tests"
	@echo "  dist       to create egg for distribution"
	@echo "  publish    to publish the package to PyPI"
	@echo

clean:
	@rm -rf build dist *.egg-info
	@find . \( -name '*.pyc' -o  -name '__pycache__' -o -name '**/*.pyc' -o -name '*~' \) -delete

deploy:
	@tsuru app-deploy -a $(project) globomap_driver_cmdb Procfile requirements.txt scheduler.py run_loader.py .python-version

test:
	@nosetests --verbose --rednose  --nocapture --cover-package=globomap_driver_cmdb; coverage report -m

dist: clean
	@python setup.py sdist

publish: clean dist
	@echo 'Ready to release version ${VERSION}? (ctrl+c to abort)' && read
	twine upload dist/*
	@git tag ${VERSION}
	@git push --tags
