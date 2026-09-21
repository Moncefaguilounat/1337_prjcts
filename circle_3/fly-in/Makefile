PYTHON := python3
MAP ?= map.txt

.PHONY: help install run visual debug clean lint lint-strict

help:
	@echo "make install          Install development dependencies for the user"
	@echo "make run MAP=file     Print the official movement output"
	@echo "make visual MAP=file  Open the colored terminal map"
	@echo "make debug MAP=file   Run the simulator with pdb"
	@echo "make clean            Remove Python and mypy caches"
	@echo "make lint             Run the mandatory subject checks"
	@echo "make lint-strict      Run the optional strict checks"

install:
	$(PYTHON) -m pip install --user -r requirements.txt

run:
	$(PYTHON) -m src.main "$(MAP)"

visual:
	$(PYTHON) -m src.main "$(MAP)" --visual

debug:
	$(PYTHON) -m pdb -m src.main "$(MAP)"

clean:
	@find src -type d -name '__pycache__' -prune -exec rm -rf {} +
	@rm -rf .mypy_cache

lint:
	$(PYTHON) -m flake8 .
	$(PYTHON) -m mypy . --warn-return-any --warn-unused-ignores \
		--ignore-missing-imports --disallow-untyped-defs \
		--check-untyped-defs

lint-strict:
	$(PYTHON) -m flake8 .
	$(PYTHON) -m mypy . --strict
