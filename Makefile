VENV := .venv
PY := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
KAGGLE := $(VENV)/bin/kaggle
UVICORN := $(VENV)/bin/uvicorn

DATA_DIR := Data
CSV := $(DATA_DIR)/movies_metadata.csv
KAGGLE_DATASET := rounakbanik/the-movies-dataset

.PHONY: setup run clean

# Setup depends on artifacts
setup: $(PY) .deps_installed $(CSV)

# Create venv only if missing
$(PY):
	python3 -m venv $(VENV)

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

run: setup
	$(UVICORN) app.main:app --reload

clean:
	rm -rf $(VENV) .deps_installed $(DATA_DIR)
