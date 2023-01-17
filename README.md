## Zenodo spam classifiers

Spam classification machine learning models for Zenodo records and communities.

## Usage

First of all, create a virtual environment (the make script will install the required dependencies in it):

```bash
   mkvirtualenv --python python3.10 zenodo-classifier # Create the virtual environment
```

To train/re-train the model:

```bash
   make train
```

The `make train` command will install all the necessary dependencies and run the following python scripts:

- `make_dataset.py`: download/create the Zenodo dataset and store it in `data/raw/zenodo_open_metadata_YYYY-MM-DD.jsonl`.
- `process_dataset.py`: extract the features/process them and store the new dataset in `data/processed/zenodo_open_metadata_processed_YYYY-MM-DD.csv`.
- `train_model.py`: train the model and store it in `models/zenodo_msc_YYYY-MM-DD`.

Note: each of these files can be called as a script (using `make` or manually) or imported as module. As a script, they don't take any parameters, the `process_dataset.py` (resp. `train_model.py`) will automatically search for the latest dataset in `data/raw/` (resp. `data/processed/`) and use it. The latest dataset is found by comparing the date present in the file name. If the data is placed manually in `data/raw` (resp. `data/processed`) it should follow the naming convention, that is, `data/raw/zenodo_open_metadata_YYYY-MM-DD.jsonl` (resp. `zenodo_open_metadata_processed_YYYY-MM-DD.csv`) to ensure that it is found automatically.

Note: checkpoints are automatically saved in `models/checkpoints/` during training. If there are some checkpoints, the training will automatically resume from there. If you want to start over for some reason, delete them.

**Note: the `make_dataset.py` script is not ready yet. In the future, it will effectively dump the Zenodo dataset in `data/raw/zenodo_open_metadata_YYYY-MM-DD.jsonl` but will remain unvailable for generic users. You should download the dataset from [this Zenodo record](https://zenodo.org/record/7438358/files/zenodo_open_metadata_2022-12-14.jsonl.gz?download=1). The results given in our report used the Zenodo dataset from 2020/10/21.**

To make a prediction on a new record you can proceed in two ways:

- Use the `predict_model.py` script:
  ```bash
  export PYTHONPATH=/path/to/zenodo-classifier # you can use "PYTHONPATH=$(pwd)" if you are in the zenodo-classifier directory
  python3 predict.py "Some description of the record that is not preprocess (but can be)"
  ```
- Import `predict_model.py` in your python script:
  ```python
  from src.models.predict_model import load_model, make_prediction
  # You need to load the model only once
  # You must pass the path to the model as argument
  # You can get the path to the latest model with `find_latest_model()` or pass the path to the model you want to use
  model = load_model(model_path)
  # You can make some predictions
  make_prediction(model, "Some description of the record that is not preprocess (but can be)")
  ```
  
To visualize the results of the model, i.e., see its performance on the test set, you can use the `visualize_results.py` script:

```bash
make visualize
```

This will generate a `report_YYYY-MM-DD.md` file in the `reports/`. To make the generate faster you can use `make visualize N=1000` to compute the results on only 1000 tests samples.

To compare with older models:

> TODO

## Structure

```

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
│   │   └── process_dataset.py
│   │
│   ├── models         <- Scripts to train models and then use trained models to make
│   │   │                 predictions
│   │   ├── predict_model.py
│   │   └── train_model.py
│   │
│   └── visualization  <- Scripts to create exploratory and results oriented visualizations
│       └── visualize.py

```
