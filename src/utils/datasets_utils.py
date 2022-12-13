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
    return pd.read_csv(processed_dataset_path)


def split_train_test(
    dataset: pd.DataFrame, test_size=0.2
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Split the dataset into train and test.

    Args:
        dataset (pd.DataFrame): Dataset to split.
        test_size (float, optional): Percentage of the dataset to use for the
        test set.

    Returns:
        pd.DataFrame, pd.DataFrame: Train and test sets.
    """
    dataset = dataset.sample(frac=1, random_state=SEED).reset_index(drop=True)
    train = dataset.iloc[: int(len(dataset) * (1 - test_size))]
    test = dataset.iloc[int(len(dataset) * (1 - test_size)) :]
    return train, test
