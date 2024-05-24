PYTHON = python
VENV := .venv
REQUIREMENTS = requirements.txt
MODULE := registraai

run:
	docker-compose up --build

venv:
	test -d $(VENV) || $(PYTHON) -m venv $(VENV)
	. $(VENV)/bin/activate && \
	$(PYTHON) -m pip install -r $(REQUIREMENTS)

generate-docs: venv
	export PYTHONPATH="./$(MODULE)/:$(PYTHONPATH)" && \
	lazydocs $(MODULE)
