"""
Dataset profiling: builds JSON-serializable summaries for LLMs and UI.
"""

from __future__ import annotations

import logging
from typing import Dict, Any

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def build_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Build a compact summary of the dataset suitable for:
    - Display in UI
    - Passing to LLMs as JSON

    Args:
        df: Input DataFrame.

    Returns:
        Dictionary with rows, cols, dtypes, missing values, numeric summary.
    """
    if df.empty:
        logger.warning("build_summary called with empty DataFrame.")
        return {
            "rows": 0,
            "cols": 0,
            "dtypes": {},
            "missing_values": {},
            "numeric_summary": {},
        }

    rows, cols = df.shape
    dtypes = df.dtypes.astype(str).to_dict()
    missing_values = df.isna().sum().to_dict()

    try:
        numeric_summary = df.describe(include=[np.number]).to_dict()
    except Exception:  # noqa: BLE001
        logger.exception("Failed to compute numeric summary.")
        numeric_summary = {}

    summary: Dict[str, Any] = {
        "rows": rows,
        "cols": cols,
        "dtypes": dtypes,
        "missing_values": missing_values,
        "numeric_summary": numeric_summary,
    }

    logger.info(
        "Built summary: %d rows, %d cols, %d numeric features",
        rows,
        cols,
        len(numeric_summary),
    )
    return summary

