# -*- coding: utf-8 -*-
# ------------------------------
# File       : init_utils.py
# Created by : Yanis De Busschere, Luka Secilmis, Thomas Ecabert
"""
Module containing utility functions and constants to initialize a scripts.

This necessary because the project is made of several standalone scripts that
need to be initialized in the same way and need to perform the same checks.
"""

import datetime
import logging
import random
import sys

import numpy as np
import torch

from src.utils.file_utils import ROOT_PATH

SEED = 42
LOG_PATH = ROOT_PATH / "logs"


def check_gpu() -> bool:
    """Check if GPU is available and log it.

    Returns:
        bool: True if GPU is available, False otherwise.
    """
    if torch.cuda.is_available():
        device = torch.device("cuda")
        logging.info(f"GPU is available. Using: {torch.cuda.get_device_name(0)}")
        return True
    else:
        logging.warning("No GPU available. Using the CPU instead.")
        return False


def init_seed(seed=SEED) -> None:
    """Set seed for reproducibility.
    Use this function and keep the same seed for all the experiments to ensure
    reproducibility.

    Args:
        seed (int, optional): Seed value. Defaults to 42.
    """
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    logging.info(f'Seed initialized to "{seed}".')


def init_logger(file_name: str, level=logging.INFO) -> None:
    """Initialize logger.

    Args:
        file_name (str): Name of the file where the logs will be stored.
    """
    if not LOG_PATH.exists():
        LOG_PATH.mkdir(parents=True)

    file_path = (
        LOG_PATH
        / f"{file_name}_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
    )
    logging.basicConfig(
        format="%(asctime)s:%(levelname)s:%(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
        level=level,
        handlers=[logging.FileHandler(file_path), logging.StreamHandler()],
    )

    sys.excepthook = lambda *args: logging.critical("Uncaught exception", exc_info=args)
