SHELL := /bin/bash

VENV := .venv
PYTHON := python3.11
PY := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
KAGGLE := $(VENV)/bin/kaggle
UVICORN := $(VENV)/bin/uvicorn

DATA_DIR := Data
CSV := $(DATA_DIR)/movies_metadata.csv
KAGGLE_DATASET := rounakbanik/the-movies-dataset

FRONTEND_DIR := frontend
FRONTEND_DEPS := $(FRONTEND_DIR)/node_modules

.PHONY: setup frontend-setup run api frontend clean

# Setup depends on artifacts
setup: $(PY) .deps_installed $(CSV)

# Create venv only if missing
$(PY):
	$(PYTHON) -m venv $(VENV)

# Install deps only if not already done
.deps_installed: requirements.txt $(PY)
	$(PIP) install -r requirements.txt
	touch .deps_installed

# Download dataset only if CSV missing
$(CSV): .deps_installed
	mkdir -p $(DATA_DIR)
	$(KAGGLE) datasets download -d $(KAGGLE_DATASET) -f movies_metadata.csv -p $(DATA_DIR)
	unzip -o $(DATA_DIR)/movies_metadata.csv.zip -d $(DATA_DIR)
	rm -f $(DATA_DIR)/movies_metadata.csv.zip

# Install frontend deps only if missing
frontend-setup: $(FRONTEND_DEPS)

$(FRONTEND_DEPS): $(FRONTEND_DIR)/package.json
	cd $(FRONTEND_DIR) && npm install

# Run API only
api: setup
	$(UVICORN) app.main:app --reload

# Run frontend only
frontend: frontend-setup
	cd $(FRONTEND_DIR) && npm run dev

# Run both API and frontend, kill both on Ctrl+C
run: setup frontend-setup
	@trap 'kill 0' INT TERM EXIT; \
	$(UVICORN) app.main:app --reload & \
	(cd $(FRONTEND_DIR) && npm run dev) & \
	wait

clean:
	rm -rf $(VENV) .deps_installed $(DATA_DIR) $(FRONTEND_DEPS)
