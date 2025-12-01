"""
Question-answering agent that uses Gemini to generate pandas code
and then executes it on an in-memory DataFrame.

Key behaviors:
- Works for ANY uploaded dataset.
- User questions do NOT need to match case or simple pluralization.
- We normalize all string columns to lowercase / singular inside the agent.
- Friendly error messages instead of raw tracebacks.
"""

from __future__ import annotations

import json
import logging
import re
from typing import Any, Tuple, Dict

import google.generativeai as genai
import numpy as np
import pandas as pd

from config import Settings, settings as default_settings

logger = logging.getLogger(__name__)


def init_qa_model(settings: Settings = default_settings) -> genai.GenerativeModel:
    """Initialize Gemini model for Q&A."""
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
            .str.rstrip("s")  # simple singular/plural handling
        )

    return df_norm


def _build_column_summary(df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
    """
    Build a lightweight summary of columns and sample values so the model
    knows what kinds of values actually exist in the dataset.
    """
    summary: Dict[str, Dict[str, Any]] = {}

    for col in df.columns:
        series = df[col]
        col_info: Dict[str, Any] = {
            "dtype": str(series.dtype),
        }

        # For text-like columns, include some unique values
        if series.dtype == "object" or pd.api.types.is_categorical_dtype(series):
            uniq = (
                series.dropna()
                .astype(str)
                .unique()[:20]
                .tolist()
            )
            col_info["sample_values"] = uniq

        summary[col] = col_info

    return summary


def run_data_query(
    model: genai.GenerativeModel,
    question: str,
    df: pd.DataFrame,
) -> Tuple[str, Any]:
    """
    Ask Gemini to generate code to answer a question about df, then execute it.

    We use a normalized copy of df for string comparisons so that user
    questions are robust to case and simple pluralization.

    Args:
        model: Gemini model.
        question: Natural-language question.
        df: Original DataFrame (not modified).

    Returns:
        Tuple of (generated_code, execution_result or error_message).
    """
    # Normalize text columns for robust matching
    df_norm = _normalize_text_df(df)

    column_names = df_norm.columns.tolist()
    col_summary = _build_column_summary(df_norm)

    prompt = f"""
You are a data analyst with access to a pandas DataFrame named df.

The DataFrame df you will use has already been NORMALIZED as follows:
- All text / categorical columns are stripped of leading/trailing spaces.
- All text is converted to lowercase.
- A trailing 's' is removed from text values to handle simple singular/plural,
  e.g. "laptop" and "laptops" are both stored as "laptop".

Here are the column names in df:
{column_names}

Here is additional information about the columns and some sample values:
{json.dumps(col_summary, indent=2)}

User question:
\"\"\"{question}\"\"\"


INSTRUCTIONS FOR WRITING CODE:

1. Use ONLY the DataFrame named `df` (the normalized one).
2. Reference column names exactly as shown above.
3. Because the text values in df are already lowercase and singularized where
   possible, you can compare them directly to lowercase singular strings.
   For example:

       df[(df['product'] == 'laptop') & (df['region'] == 'north')]['units_sold'].sum()

4. Do NOT import any modules (assume pandas as pd and numpy as np are available).
5. Your code must evaluate directly to the final answer. If you write multiple
   lines, ensure the final answer is in a variable called `result`.

6. If you filter df and end up with NO MATCHING ROWS, do NOT call idxmax()
   or other operations that require non-empty data. Instead, either return 0
   or a short explanatory string like "No rows matched the condition ...".

Return ONLY the Python code that produces the answer.
Do NOT include explanations, comments, markdown, or backticks.
"""

    logger.info("Asking Gemini to generate code for question: %s", question)

    response = model.generate_content(prompt)
    raw_code = response.text or ""
    code = _clean_model_code(raw_code)

    logger.debug("Raw code from Gemini: %s", raw_code)
    logger.info("Cleaned code to execute: %s", code)

    # Restricted execution environment
    safe_globals = {"__builtins__": {}}
    safe_locals = {
        "df": df_norm,  # IMPORTANT: use normalized DataFrame here
        "pd": pd,
        "np": np,
    }

    try:
        # First, try evaluating as a single expression
        try:
            compiled = compile(code, "<llm_code>", "eval")
            result = eval(compiled, safe_globals, safe_locals)
        except SyntaxError:
            # Otherwise treat it as a statement block and expect `result`
            compiled = compile(code, "<llm_code>", "exec")
            exec(compiled, safe_globals, safe_locals)
            result = safe_locals.get("result", None)

        # If the result is a pandas object and empty, explain that nicely.
        if isinstance(result, (pd.Series, pd.DataFrame)) and result.empty:
            friendly = (
                "The generated code ran successfully, but it produced an empty result.\n\n"
                "This usually means the filter condition did not match any rows in the "
                "dataset. Try checking the dataset preview for the values that exist "
                "and rephrase your question."
            )
            return code, friendly

        return code, result

    except Exception as exc:  # noqa: BLE001
        logger.exception("Error while executing generated code.")
        msg = str(exc)

        # Special handling for argmax-on-empty issues.
        if "argmax" in msg and "empty" in msg:
            friendly = (
                "The code tried to compute a maximum (e.g. using idxmax), "
                "but the data it was working on was empty.\n\n"
                "This usually happens when the filter condition removed all rows. "
                "Please check the values shown in the dataset preview and try again."
            )
            return code, friendly

        generic = (
            "Error executing generated code:\n"
            f"{type(exc).__name__}: {exc}"
        )
        return code, generic
