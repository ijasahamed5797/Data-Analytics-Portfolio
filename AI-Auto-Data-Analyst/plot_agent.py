"""
Plot agent: uses Gemini to generate matplotlib/seaborn code
and returns a matplotlib Figure for Streamlit to display.
"""

from __future__ import annotations

import json
import logging
import re
from typing import Any, Tuple, Dict

import google.generativeai as genai
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from config import Settings, settings as default_settings

logger = logging.getLogger(__name__)


def init_plot_model(settings: Settings = default_settings) -> genai.GenerativeModel:
    """Initialize Gemini model for visualization prompts."""
    genai.configure(api_key=settings.gemini_api_key)
    model = genai.GenerativeModel(settings.gemini_model_name)
    return model


def _clean_model_code(raw_code: str) -> str:
    """Remove markdown fences / language tags from LLM output."""
    code = (raw_code or "").strip()
    code = re.sub(r"```python", "", code, flags=re.IGNORECASE)
    code = re.sub(r"```", "", code).strip()
    return code


def _normalize_text_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create a normalized copy of df where:
    - all object/category columns are stripped, lowercased,
      and have a trailing 's' removed for simple plurals.
    """
    df_norm = df.copy()

    obj_cols = df_norm.select_dtypes(include=["object", "category"]).columns
    for col in obj_cols:
        df_norm[col] = (
            df_norm[col]
            .astype(str)
            .str.strip()
            .str.lower()
            .str.rstrip("s")
        )

    return df_norm


def _build_column_summary(df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
    """Summarise columns + some sample values for the model."""
    summary: Dict[str, Dict[str, Any]] = {}
    for col in df.columns:
        series = df[col]
        info: Dict[str, Any] = {"dtype": str(series.dtype)}
        if series.dtype == "object" or pd.api.types.is_categorical_dtype(series):
            info["sample_values"] = (
                series.dropna().astype(str).unique()[:20].tolist()
            )
        summary[col] = info
    return summary


def run_plot_query(
    model: genai.GenerativeModel,
    question: str,
    df: pd.DataFrame,
) -> Tuple[str, Any]:
    """
    Ask Gemini to generate plotting code to visualise df, then execute it.

    Returns:
        (generated_code, result)
        where result is:
          - a matplotlib Figure,
          - a list of Figures, or
          - an error / info string.
    """
    df_norm = _normalize_text_df(df)

    column_names = df_norm.columns.tolist()
    col_summary = _build_column_summary(df_norm)

    prompt = f"""
You are a data visualization expert with access to a pandas DataFrame named df.

The DataFrame df has already been NORMALIZED:
- text columns are stripped and lowercased
- simple plural 's' has been removed (e.g. "laptop" and "laptops" → "laptop")

Here are the columns in df:
{column_names}

Here is additional information about the columns:
{json.dumps(col_summary, indent=2)}

User request for a chart:
\"\"\"{question}\"\"\"


INSTRUCTIONS:

1. Use pandas, numpy (np), matplotlib.pyplot as plt, and optionally seaborn as sns.
2. Do NOT import any modules (assume they are already imported).
3. Use ONLY the DataFrame named df (the normalized one).
4. Create ONE main matplotlib Figure object and assign it to a variable called `fig`.
   - You may create subplots inside that figure if needed.
5. Do NOT call plt.show() or save figures to disk.
6. The last line of your code should leave `fig` defined as the Figure to display.

Return ONLY the Python code, no explanations, no comments, no markdown.
"""

    logger.info("Asking Gemini to generate plot code for: %s", question)
    response = model.generate_content(prompt)
    raw_code = response.text or ""
    code = _clean_model_code(raw_code)

    logger.debug("Raw plot code from Gemini: %s", raw_code)
    logger.info("Cleaned plot code to execute: %s", code)

    # Restricted execution environment
    safe_globals = {"__builtins__": {}}
    safe_locals = {
        "df": df_norm,
        "pd": pd,
        "np": np,
        "plt": plt,
        "sns": sns,
    }

    try:
        compiled = compile(code, "<plot_code>", "exec")
        exec(compiled, safe_globals, safe_locals)

        fig = safe_locals.get("fig", None)

        # One figure
        from matplotlib.figure import Figure
        if isinstance(fig, Figure):
            return code, fig

        # If model created multiple figures, allow list
        figs = safe_locals.get("figs", None)
        if isinstance(figs, list) and all(
            isinstance(f, Figure) for f in figs
        ):
            return code, figs

        # Fallback if nothing usable is returned
        return code, (
            "The code ran but did not produce a `fig` or `figs` object. "
            "Please try rephrasing your chart request."
        )

    except Exception as exc:  # noqa: BLE001
        logger.exception("Error while executing generated plot code.")
        return code, f"Error executing generated plot code: {type(exc).__name__}: {exc}"
