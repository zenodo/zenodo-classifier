#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------
# File       : train_dataset.py
# Created by : Yanis De Busschere, Luka Secilmis, Thomas Ecabert
"""Module/script used to train a new model on the processed dataset."""

import logging
from pathlib import Path
import shutil

import datasets
import evaluate
import numpy as np
import pandas as pd
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    Trainer,
    TrainingArguments,
    logging as transformers_logging,
)

from src.utils.datasets_utils import load_processed_dataset, split_train_test
from src.utils.file_utils import (
    MODEL_CHECKPOINTS_PATH,
    MODELS_PATH,
    extract_date,
    find_latest_processed_dataset,
)
from src.utils.init_utils import SEED, check_gpu, init_logger, init_seed


def tokenize(train: pd.DataFrame, test: pd.DataFrame) -> pd.DataFrame:
    """Tokenizes the dataset.

    Args:
        train (pd.DataFrame): Train dataset.
        test (pd.DataFrame): Test dataset.

    Returns:
        pd.DataFrame: Tokenized dataset
    """
    logging.info("Tokenizing dataset.")
    tokenizer = AutoTokenizer.from_pretrained("distilbert-base-multilingual-cased")

    train = pd.DataFrame(
        {
            "label": [int(x) for x in train["label"].tolist()],
            "text": [str(x) for x in train["description"].tolist()],
        }
    )

    test = pd.DataFrame(
        {
            "label": [int(x) for x in test["label"].tolist()],
            "text": [str(x) for x in test["description"].tolist()],
        }
    )

    dataset = datasets.DatasetDict(
        {
            "train": datasets.Dataset.from_dict(train),
            "test": datasets.Dataset.from_dict(test),
        }
    )
    dataset_tokenized = dataset.map(
        lambda e: tokenizer(e["text"], padding="max_length", truncation=True),
        batched=True,
    )

    logging.info("Tokenization finished.")
    return dataset_tokenized


def compute_metrics(eval_pred):
    """Computes metrics for the model.

    Args:
        eval_pred (tuple): Tuple containing the predictions and the labels.

    Returns:
    """
    metric = evaluate.combine(["accuracy", "f1"])
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    results = metric.compute(predictions=predictions, references=labels, seed=SEED)
    logging.info(f"Metrics: {results}")
    return results


def train_model(
    processed_dataset_path: Path, model_path: Path, model_checkpoints_path: Path
) -> None:
    """Trains the model and save it.

    Args:
        processed_dataset_path (str): Path to the processed dataset.
        model_path (str): Path to the model.
        model_checkpoints_path (str): Path to the model checkpoints.
    """

    dataset = load_processed_dataset(processed_dataset_path)
    train, test = split_train_test(dataset)

    dataset_tokenized = tokenize(train, test)

    model = AutoModelForSequenceClassification.from_pretrained(
        "distilbert-base-multilingual-cased", num_labels=2
    )

    training_args = TrainingArguments(
        output_dir=model_checkpoints_path,
        overwrite_output_dir=True,
        save_total_limit=2,
        seed=SEED,
        log_level="info",
        logging_strategy="steps",
        logging_steps=2500,
        evaluation_strategy="steps",
        eval_steps=2500,
        save_strategy="steps",
        save_steps=2500,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset_tokenized["train"],
        eval_dataset=dataset_tokenized["test"],
        compute_metrics=compute_metrics,
    )

    if (
        model_checkpoints_path.exists()
        and len(list(model_checkpoints_path.iterdir())) > 0
    ):
        logging.info(
            f"Files found in {model_checkpoints_path}, trying to resume training."
        )
        resume_from_checkpoint = True
    else:
        logging.info(
            f"No files found in {model_checkpoints_path}, starting training from scratch."
        )
        resume_from_checkpoint = False

    trainer.train(resume_from_checkpoint=resume_from_checkpoint)
    logging.info("Training finished.")

    trainer.evaluate()

    trainer.save_model(model_path)
    logging.info(f"Model saved in {model_path}.")

    logging.info(f"Deleting checkpoints in {model_checkpoints_path}.")
    shutil.rmtree(model_checkpoints_path)
    logging.info(f"Deleted {model_checkpoints_path}.")


if __name__ == "__main__":
    init_logger("train_model")
    transformers_logging.set_verbosity_info()
    transformers_logging.disable_default_handler()
    transformers_logging.disable_progress_bar()
    transformers_logging.add_handler(logging.getLogger())
    evaluate.logging.set_verbosity_info()
    evaluate.logging.get_logger().addHandler(logging.getLogger())

    init_seed()
    check_gpu()

    processed_dataset_path = find_latest_processed_dataset()
    if not processed_dataset_path.exists():
        logging.critical(f"Processed dataset not found at {processed_dataset_path}")
        exit(1)

    date = extract_date(processed_dataset_path.name)

    model_path = MODELS_PATH / f"model_msc_{date}"
    if model_path.exists():
        # This is critical because we quit the program but we return 0 to ensure
        # that the pipeline does not fail entirely.
        logging.critical(f"Model already exists at {model_path}")
        exit(0)

    model_checkpoints_path = MODEL_CHECKPOINTS_PATH / f"checkpoints_model_msc_{date}"

    train_model(processed_dataset_path, model_path, model_checkpoints_path)
