"""
LLM (Gemini) integration for generating dataset insights.
"""

from __future__ import annotations

import json
import logging
from typing import Dict, Any

import google.generativeai as genai

from config import Settings, settings as default_settings

logger = logging.getLogger(__name__)


def init_gemini(settings: Settings = default_settings) -> genai.GenerativeModel:
    """
    Initialize the Gemini model.

    Args:
        settings: App settings with API key and model name.

    Returns:
        Configured GenerativeModel instance.
    """
    logger.info("Initializing Gemini with model %s", settings.gemini_model_name)
    genai.configure(api_key=settings.gemini_api_key)
    model = genai.GenerativeModel(settings.gemini_model_name)
    return model


def generate_insights(model: genai.GenerativeModel, summary: Dict[str, Any]) -> str:
    """
    Generate a natural-language EDA report from dataset summary.

    Args:
        model: Gemini generative model.
        summary: Dataset summary as produced by profiling.build_summary.

    Returns:
        Human-readable multi-section report string.
    """
    prompt = f"""
You are a senior data analyst.

You are given a dataset summary in JSON format:

{json.dumps(summary, indent=2)}

Please provide a structured analysis with headings:

1. Dataset Overview
2. Key Statistical Insights
3. Data Quality Issues (missing values, outliers, etc.)
4. Relationships & Patterns (if possible from numeric summary)
5. Potential Business Insights
6. Recommended Next Steps (further analysis or ML tasks)

Write clearly and concisely.
"""

    try:
        logger.info("Requesting insights from Gemini.")
        response = model.generate_content(prompt)
        text = response.text or "(No response text received.)"
        logger.info("Received insights from Gemini (%d characters).", len(text))
        return text
    except Exception as exc:  # noqa: BLE001
        logger.exception("Error while generating insights from Gemini.")
        return f"Error while generating insights from Gemini: {exc}"
