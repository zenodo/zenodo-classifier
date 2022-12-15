#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------
# File       : predict_model.py
# Created by : Yanis De Busschere, Luka Secilmis, Thomas Ecabert
"""Module/script used to load a model and make predictions on new data."""

import logging
import sys

from transformers import (
    Pipeline,
    pipeline,
    AutoModelForSequenceClassification,
    AutoTokenizer,
)
from src.features.process_dataset import parse_description
from src.utils.file_utils import MODELS_PATH, find_latest_model
from src.utils.init_utils import check_gpu, init_logger


def load_model(model_path: str) -> Pipeline:
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    model_tokenizer = AutoTokenizer.from_pretrained(
        "distilbert-base-multilingual-cased"
    )
    classifier = pipeline("text-classification", model=model, tokenizer=model_tokenizer)
    return classifier


def make_prediction(description: str, model: Pipeline) -> bool:
    """Makes a prediction on a description. The description doesn't have to be
    preprocessed.

    Args:
        description (str): Description to predict.
        model (Pipeline): Model to use for prediction.

    Returns:
        bool: Prediction. True if the description is spam, False otherwise.
    """
    description = parse_description(description)
    prediction = model(description, padding=True, truncation=True)
    is_spam = prediction[0]["label"] == "LABEL_1"
    score = prediction[0]["score"]
    logging.debug(f'Prediction for "{description}": {is_spam=}, {score=}')
    return is_spam


if __name__ == "__main__":
    init_logger("predict_model")

    if len(sys.argv) != 2:
        logging.critical("Usage: predict_model <description>")

    model_path = find_latest_model()
    if model_path is None or not model_path.exists():
        logging.critical(f"Model not found in {MODELS_PATH}.")
        sys.exit(1)

    check_gpu()

    model = load_model(model_path)
    description = sys.argv[1]
    make_prediction(description, model)
