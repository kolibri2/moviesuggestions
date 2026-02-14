DATA_DIR := Data
KAGGLE_DATASET := rounakbanik/the-movies-dataset
CSV := $(DATA_DIR)/movies_metadata.csv

.PHONY: data run
data: $(CSV)

$(CSV):
	mkdir -p $(DATA_DIR)
	kaggle datasets download -d $(KAGGLE_DATASET) -f movies_metadata.csv -p $(DATA_DIR)
	unzip -o $(DATA_DIR)/movies_metadata.csv.zip -d $(DATA_DIR)
	rm -f $(DATA_DIR)/movies_metadata.csv.zip
	@test -f $(CSV) && echo "OK: $(CSV) ready" || (echo "Missing $(CSV)" && exit 1)

run: data
	uvicorn app.main:app --reload
