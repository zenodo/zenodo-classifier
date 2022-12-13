#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------
# File       : process_dataset.py
# Created by : Yanis De Busschere, Luka Secilmis, Thomas Ecabert
"""Module/script used to process the raw dataset."""

import logging
import sys
from math import ceil

from bs4 import BeautifulSoup
import pandas as pd

from src.utils.file_utils import (
    PROCESSED_DATASETS_EXTENSION,
    PROCESSED_DATASETS_PREFIX,
    RAW_DATASETS_PATH,
    PROCESSED_DATASETS_PATH,
    extract_date,
    find_latest_raw_dataset,
)

from src.utils.init_utils import init_logger, init_seed, SEED

KEPT_FIELDS = ["description", "spam"]
CHUNK_SIZE = 100000


def parse_description(description: str) -> str:
    """Cleans up the description by removing HTML tags.

    Args:
        description (str): Description to clean up.

    Returns:
        str: Cleaned up description.
    """
    return BeautifulSoup(description, "html.parser").get_text()


def process_dataset(raw_dataset_path: str, processed_dataset_path: str) -> None:
    """Process the raw dataset, process it and save it.

    Args:
        raw_dataset_path (str): Path to the raw dataset.
        processed_dataset_path (str): Path to the processed dataset.
    """

    spams = pd.DataFrame()
    hams = pd.DataFrame()

    logging.info(f'Processing dataset from "{raw_dataset_path}".')
    logging.info(f'Processed dataset will be saved to "{processed_dataset_path}".')

    nb_lines = 0
    with open(raw_dataset_path, "r") as f:
        for _ in f:
            nb_lines += 1
    chunk_done = 0

    for chunk in pd.read_json(raw_dataset_path, lines=True, chunksize=CHUNK_SIZE):
        logging.info(
            f"Processing chunk {chunk_done + 1} out of {ceil(nb_lines / CHUNK_SIZE)}."
        )

        chunk = chunk[KEPT_FIELDS].dropna()

        chunk_spams = chunk[chunk["spam"] == True]
        chunk_spams["description"] = chunk_spams["description"].map(parse_description)
        chunk_spams = chunk_spams.assign(spam=1)
        spams = pd.concat([spams, chunk_spams]).dropna()

        chunk_hams = chunk[chunk["spam"] == False]
        chunk_hams["description"] = chunk_hams["description"].map(parse_description)
        chunk_hams = chunk_hams.assign(spam=0)
        hams = pd.concat([hams, chunk_hams]).dropna()

        chunk_done += 1

    hams = hams.sample(n=2 * len(spams), random_state=SEED)

    df = pd.concat([spams, hams]).rename(columns={"spam": "label"})
    df.to_csv(processed_dataset_path, index=False)
    logging.info(f'Dataset processed and saved to "{processed_dataset_path}".')


if __name__ == "__main__":
    init_logger("process_dataset")
    init_seed()

    raw_dataset_path = find_latest_raw_dataset()
    if raw_dataset_path is None or not raw_dataset_path.exists():
        logging.critical(f"No raw dataset found in {RAW_DATASETS_PATH}.")
        sys.exit(1)

    date = extract_date(raw_dataset_path.name)
    processed_dataset_path = (
        PROCESSED_DATASETS_PATH
        / f"{PROCESSED_DATASETS_PREFIX}{date}{PROCESSED_DATASETS_EXTENSION}"
    )

    if processed_dataset_path.exists():
        # This is critical because we quit the program but we return 0 to ensure
        # that the pipeline does not fail entirely.
        logging.critical(
            f"Processed dataset already exists at {processed_dataset_path}."
        )
        sys.exit(0)

    process_dataset(raw_dataset_path, processed_dataset_path)
