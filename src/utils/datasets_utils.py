# -*- coding: utf-8 -*-
# ------------------------------
# File       : datasets_utils.py
# Created by : Yanis De Busschere, Luka Secilmis, Thomas Ecabert
"""
Module containing utility functions to handle datasets, for example, load 
and split.
"""

from typing import Tuple

import pandas as pd

from src.utils.init_utils import SEED


def load_processed_dataset(processed_dataset_path: str) -> pd.DataFrame:
    """Load the processed dataset.

    Returns:
        pd.DataFrame: Preprocessed dataset.
    """
    return pd.read_pickle(processed_dataset_path)


def split_train_test(
    dataset: pd.DataFrame, test_size=0.2
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Split the dataset into train and test. It will keep exactly the same
    distribution of classes in both train and test.

    Args:
        dataset (pd.DataFrame): Dataset to split.
        test_size (float, optional): Percentage of the dataset to use for the
        test set.

    Returns:
        pd.DataFrame, pd.DataFrame: Train and test sets.
    """
    spams = dataset[dataset["label"] == 1]
    hams = dataset[dataset["label"] == 0]

    spams = spams.sample(frac=1, random_state=SEED)
    hams = hams.sample(frac=1, random_state=SEED)

    spams_train = spams[: int(len(spams) * (1 - test_size))]
    spams_test = spams[int(len(spams) * (1 - test_size)) :]
    hams_train = hams[: int(len(hams) * (1 - test_size))]
    hams_test = hams[int(len(hams) * (1 - test_size)) :]

    train = pd.concat([spams_train, hams_train])
    test = pd.concat([spams_test, hams_test])

    train = train.sample(frac=1, random_state=SEED)
    test = test.sample(frac=1, random_state=SEED)

    return train, test
