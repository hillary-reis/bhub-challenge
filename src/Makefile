PROJECT_NAME := bhub-api-challenge
PYTHON_VERSION := 3.11.1
VENV_NAME := $(PROJECT_NAME)-$(PYTHON_VERSION)
COVERAGE := 95

create-venv:
	pyenv install -s $(PYTHON_VERSION)
	pyenv global ${PYTHON_VERSION}
	poetry env use ${PYTHON_VERSION}
	poetry shell


.set-python-version:
	pyenv global ${PYTHON_VERSION}


.flake:
	echo "Running flake8"
	python -m flake8 bhub --output-file=test-results/flake8.txt


.bandit:
	echo "Running bandit"
	bandit -o test-results/bandit_report.json -f json -r bhub -c ../.bandit


.prepare-result-directory:
	rm -rf test-results
	mkdir -p test-results


code-analysis: .prepare-result-directory .bandit .flake


test:
	pytest -vv --cov=. --cov-report=term-missing --cov-report=html --cov-fail-under=$(COVERAGE)


## remove Python file artifacts
.clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +


## remove test and coverage artifacts
.clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr reports/
	rm -fr .pytest_cache/
	rm -f coverage.xml


clean: .clean-pyc .clean-test
