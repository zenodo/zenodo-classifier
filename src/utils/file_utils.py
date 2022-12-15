# -*- coding: utf-8 -*-
# ------------------------------
# File       : file_utils.py
# Created by : Yanis De Busschere, Luka Secilmis, Thomas Ecabert
"""
Module containing utility functions and constants to access and find
files in the project.
"""

import logging
from pathlib import Path
import re


ROOT_PATH = Path(__file__).parents[2]

DATA_PATH = ROOT_PATH / "data"

RAW_DATASETS_PATH = DATA_PATH / "raw"
RAW_DATASETS_PREFIX = "zenodo_open_metadata_"
RAW_DATASETS_EXTENSION = ".jsonl"

PROCESSED_DATASETS_PATH = DATA_PATH / "processed"
PROCESSED_DATASETS_PREFIX = RAW_DATASETS_PREFIX + "processed_"
PROCESSED_DATASETS_EXTENSION = ".csv"


MODELS_PATH = ROOT_PATH / "models"
MODELS_PREFIX = "model_msc_"
MODELS_EXTENSION = ""

MODEL_CHECKPOINTS_PATH = MODELS_PATH / "checkpoints"

REPORTS_PATH = ROOT_PATH / "reports"


def extract_date(filename: str) -> str | None:
    """Extract the date from the filename.

    Args:
        filename (str): Filename

    Returns:
        str: Date
    """
    match = re.match(r".*_(\d{4}-\d{1,2}-\d{1,2}).*", filename)
    if match:
        return match.group(1)
    return None


def find_latest_in_directory(
    directory: str, prefix: str, extension: str
) -> Path | None:
    """Find the latest file in a directory. The latest file is the one with
    the latest timestamp in its name.

    Args:
        directory (str): Directory where to search for the latest file.
        prefix (str): Prefix of the file to search.
        extension (str): Extension of the file to search, e.g. ".csv".


    Returns:
        str: Absolute path of the latest file.
    """
    logging.debug(f"Searching for latest file in {directory}")
    oldest = None
    oldest_date = None
    for file in directory.iterdir():
        pattern = prefix + r"(\d{4}-\d{1,2}-\d{1,2})" + extension
        match = re.match(pattern, file.name)
        if match:
            logging.debug(f"Found file {file.name}")
            date = match.group(1)
            if not oldest_date or date < oldest_date:
                logging.debug(f"File {file.name} is the oldest so far.")
                oldest_date = date
                oldest = file
        else:
            if not file.name.startswith("."):
                logging.debug(
                    f"File {file.name} does not match the pattern: {pattern} but is present in the directory."
                )
    if oldest:
        return oldest.absolute()
    return None


def find_latest_raw_dataset() -> str:
    """Find the latest raw dataset in the raw datasets directory.

    Returns:
        str: Absolute path of the latest raw dataset.
    """
    return find_latest_in_directory(
        RAW_DATASETS_PATH, RAW_DATASETS_PREFIX, RAW_DATASETS_EXTENSION
    )


def find_latest_processed_dataset() -> str:
    """Find the latest processed dataset in the processed datasets directory.

    Returns:
        str: Absolute path of the latest processed dataset.
    """
    return find_latest_in_directory(
        PROCESSED_DATASETS_PATH, PROCESSED_DATASETS_PREFIX, PROCESSED_DATASETS_EXTENSION
    )


def find_latest_model() -> str:
    """Find the latest model in the models directory.

    Returns:
        str: Absolute path of the latest model.
    """
    return find_latest_in_directory(MODELS_PATH, MODELS_PREFIX, MODELS_EXTENSION)
