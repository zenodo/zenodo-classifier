# Zenodo spam classifiers

Spam classification machine learning models for Zenodo records and communities.

## Usage

First of all, create a virtualenv, install the depencencies, and run the Jupyter notebook server:

```bash
mkvirtualenv --python python3.6 zenodo-classifier
(zenodo-classifier) pip install -r requirements.txt
# This will also open Kupyter notebook in your browser
(zenodo-classifier) jupyter notebook
```

To re-train the model:

1. Run the `dump_zenodo_open_metadata.py` script in production to generate the latest dump
2. Download the dump locally
3. Open the `model_spam_detection_record.ipynb` notebook
4. Update the `data_file` and `model_path` variables to point to the new dump location
5. Run all the cells up to `4. Dump model`.

To compare with older models:

> TODO

## Structure

- `datasets/` - Downloaded datasets
- `models/` - "Pickled" trained models
- `experiments/` - Experimental model notebooks
- `legacy/` - Legacy model notebooks
- `dump_zenodo_open_metadata.py` - Generates a dump from the database, that can be used to train classifier models
- `download_zenodo_open_metadata_archive.py` - Downloads and extracts older dumps
- `clean_zenodo_open_metadata.py` - Cleans downloaded datasets
- `model_spam_detection_record.ipynb` + `model_spam_detection_communities.ipynb` - Currently used classifier model notebooks for producing a trained model

### TODO

- [ ] Update communities model
- [ ] Improve metrics
- [ ] Update README
