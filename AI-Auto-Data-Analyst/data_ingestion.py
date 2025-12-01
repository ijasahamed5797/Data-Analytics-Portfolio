"""
Data ingestion and basic validation utilities.
"""

from __future__ import annotations

import logging
from typing import Tuple, List

import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


def load_csv(file_path: str, encoding: str | None = None) -> pd.DataFrame:
    """
    Load a CSV file into a pandas DataFrame.

    Args:
        file_path: Path to the CSV file.
        encoding: Optional file encoding.

    Returns:
        Loaded DataFrame.

    Raises:
        FileNotFoundError: If file does not exist.
        ValueError: If DataFrame is empty.
    """
    logger.info("Loading CSV from %s", file_path)
    try:
        df = pd.read_csv(file_path, encoding=encoding)
    except FileNotFoundError as exc:
        logger.error("File not found: %s", file_path)
        raise
    except Exception as exc:  # noqa: BLE001
        logger.exception("Unexpected error while reading CSV")
        raise ValueError(f"Unable to read CSV: {exc}") from exc

    if df.empty:
        msg = "Loaded DataFrame is empty."
        logger.error(msg)
        raise ValueError(msg)

    logger.info("Loaded DataFrame with shape %s", df.shape)
    return df


def infer_column_types(df: pd.DataFrame) -> Tuple[List[str], List[str]]:
    """
    Infer numeric and categorical columns from a DataFrame.

    Args:
        df: Input DataFrame.

    Returns:
        Tuple of (numeric_columns, categorical_columns).
    """
    if df.empty:
        logger.warning("infer_column_types called with empty DataFrame.")
        return [], []

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()

    logger.info(
        "Inferred %d numeric and %d categorical columns",
        len(numeric_cols),
        len(categorical_cols),
    )
    return numeric_cols, categorical_cols
