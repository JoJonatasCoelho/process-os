VENV := venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

.DEFAULT_GOAL := help

help:
	@echo "Comandos disponíveis:"
	@sed -n 's/^##//p' $(MAKEFILE_LIST) | column -t -s ':' |  sed -e 's/^/ /'

venv:
	test -d $(VENV) || python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	test -f requirements.txt && $(PIP) install -r requirements.txt || echo "requirements.txt não encontrado."

runq1: venv
	$(PYTHON) ex1/main.py

runq2: venv
	$(PYTHON) ex2/main.py

runq3: venv
	$(PYTHON) ex3/main.py

clean:
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -exec rm -f {} +

setup: clean venv

.PHONY: help venv runq1 runq2 runq3 clean setup