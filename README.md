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

1. Go to Zenodo Open Metadata record `https://doi.org/10.5281/zenodo.787062` to acces all dataset versions
2. Download the latest dump locally under `datasets`
3. Open the `model_spam_detection_record.ipynb` notebook
4. Update the `data_file` and `model_path` variables to point to the new dump location
5. Run all the cells up to `4. Dump model`.

To compare with older models:

> TODO

## Structure

- `experiments/` - Experimental model notebooks
- `legacy/` - Legacy model notebooks
- `notebooks/` - All notebook files. 
	- `model_spam_detection_record.ipynb` + `model_spam_detection_communities.ipynb` - Currently used classifier model notebooks for producing a trained model
	- `run_model_py.ipynb`
- `datasets/` - Locally created, dataset directory.


