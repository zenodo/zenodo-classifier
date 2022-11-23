# Zenodo spam classifiers

Spam classification machine learning models for Zenodo records and communities.

## Usage

First of all, create a virtualenv, install the depencencies, and run the Jupyter notebook server:

```bash
# Create a virtual environment
   mkvirtualenv --python python3.9 zenodo-classifier
   (zenodo-classifier) pip install -r requirements.txt
   
# This will also open Jupyter notebook in your browser
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

------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── experiments        <- Experimental model notebooks, previously trained
    │
    ├── legacy             <- Legacy model notebooks
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py

--------


