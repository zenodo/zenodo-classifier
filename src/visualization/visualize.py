import time
import logging
from pathlib import Path
import pandas as pd
import sys

from sklearn.metrics import confusion_matrix

from src.utils.init_utils import init_logger, init_seed
from src.utils.file_utils import (
    REPORTS_PATH,
    MODELS_PATH,
    extract_date,
    find_latest_model,
    PROCESSED_DATASETS_PATH,
    PROCESSED_DATASETS_EXTENSION,
    PROCESSED_DATASETS_PREFIX,
)
from src.models.predict_model import load_model, make_prediction
from src.utils.datasets_utils import load_processed_dataset, split_train_test
from src.features.process_dataset import parse_description


PDF_WIDTH = 210
PDF_HEIGHT = 297
NUM_FP_TO_SHOW = 10
NUM_FN_TO_SHOW = 10
MAX_LINES_TO_SHOW = 3


def make_predictions_with_time(model, expected_df):
    total_time = 0
    count = 0
    predictions_df = pd.DataFrame(
        {
            "description": pd.Series(dtype=str),
            "label": pd.Series(dtype=bool),
        }
    )
    for _, row in expected_df.iterrows():
        start_time = time.time()
        prediction = make_prediction(row["description"], model)
        prediction_time = time.time() - start_time
        total_time += prediction_time
        predictions_df = pd.concat(
            [
                predictions_df,
                pd.DataFrame(
                    {
                        "description": [row["description"]],
                        "label": [prediction],
                    }
                ),
            ]
        )

        count += 1
        logging.info(
            f"Example {count} done in {prediction_time:.4f} seconds. Average time: {total_time / (count):.4f} seconds."
        )
    predictions_df.reset_index(drop=True, inplace=True)
    return predictions_df, total_time / count


def generate_report(model_path: Path, N=None):
    """Generate a report for a model.

    Args:
        model_path (Path): Path to the model.
        N (int, optional): Number of examples to use for the report. None means
            all examples. Defaults to None.
    """
    logging.info(f"Generating report for model {model_path} and N={N}.")
    model = load_model(model_path)

    date = extract_date(model_path.name)
    processed_dataset_path = (
        PROCESSED_DATASETS_PATH
        / f"{PROCESSED_DATASETS_PREFIX}{date}{PROCESSED_DATASETS_EXTENSION}"
    )
    if not processed_dataset_path.exists():
        logging.critical(f"Processed dataset {processed_dataset_path} not found.")
        sys.exit(1)

    expected_df = split_train_test(load_processed_dataset(processed_dataset_path))
    expected_df = expected_df[1].dropna()
    expected_df = expected_df[:N]
    expected_df["label"] = expected_df["label"].astype(bool)
    expected_df.reset_index(drop=True, inplace=True)

    predictions_df, average_time = make_predictions_with_time(model, expected_df)

    report_path = REPORTS_PATH / f"report_{date}.md"
    logging.info(f"Saving report to {report_path}.")
    if report_path.exists():
        logging.warning(f"Report {report_path} already exists. Overwriting.")

    with open(report_path, "w") as f:
        f.write(f"# Report for model {model_path.name}\n")

        f.write("\n")
        f.write("## Predictions")
        f.write("\n")
        f.write(f" - Number of examples: {len(expected_df)}\n")
        f.write(f" - Number of spam labels: {expected_df['label'].sum()}\n")
        f.write(f" - Number of ham examples: {len(expected_df) - expected_df['label'].sum()}\n")
        f.write(f" - Average prediction time: {average_time:.2f}s\n")

        f.write("\n")
        f.write("## Confusion matrix")
        f.write("\n")
        confusion_matrix_df = pd.DataFrame(
            confusion_matrix(expected_df["label"], predictions_df["label"]),
            columns=["Pred. Ham", "Pred. Spam"],
            index=["Actual Ham", "Actual Spam"],
        )
        f.write(confusion_matrix_df.to_markdown())

        f.write("\n\n")
        confusion_matrix_df = pd.DataFrame(
            confusion_matrix(
                expected_df["label"], predictions_df["label"], normalize="true"
            ),
            columns=["Pred. Ham", "Pred. Spam"],
            index=["Actual Ham", "Actual Spam"],
        )
        f.write(confusion_matrix_df.to_markdown())

        f.write("\n\n")
        f.write("## Examples of False Positive\n")
        f.write("\n")
        f.write("Samples that were classified as spam but are actually ham.\n")
        f.write("\n")
        count = 0
        for _, row in predictions_df.iterrows():
            if count >= NUM_FP_TO_SHOW:
                break
            if row["label"] and not expected_df.iloc[row.name]["label"]:
                count += 1
                f.write("```\n")
                split_lines = parse_description(row["description"]).split("\n")
                for line in split_lines[:MAX_LINES_TO_SHOW]:
                    f.write(line + "\n")
                f.write("```\n")

        f.write("\n")
        f.write("## Examples of False Negative\n")
        f.write("\n")
        f.write("Samples that were classified as ham but are actually spam.\n")
        f.write("\n")
        count = 0
        for _, row in predictions_df.iterrows():
            if count >= NUM_FN_TO_SHOW:
                break
            if not row["label"] and expected_df.iloc[row.name]["label"]:
                count += 1
                f.write("```\n")
                split_lines = parse_description(row["description"]).split("\n")
                for line in split_lines[:MAX_LINES_TO_SHOW]:
                    f.write(line + "\n")
                f.write("```\n")
    logging.info(f"Report saved to {report_path}.")

if __name__ == "__main__":
    init_logger("visualize")
    init_seed()

    if len(sys.argv) > 2:
        logging.critical("Usage: python visualize.py [<nb_examples>]")
        sys.exit(1)

    N = None
    if len(sys.argv) == 2:
        N = int(sys.argv[1])

    generate_report(find_latest_model(), N=N)
