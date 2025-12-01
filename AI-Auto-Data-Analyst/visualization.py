"""
Visualization pipeline using matplotlib / seaborn.
Returns matplotlib Figure objects so UI layers can decide how to render them.
"""

from __future__ import annotations

import logging
from typing import List, Dict

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

logger = logging.getLogger(__name__)


def create_histograms(df: pd.DataFrame, numeric_cols: List[str]) -> Dict[str, plt.Figure]:
    """
    Create histogram plots for each numeric column.

    Returns:
        Mapping from column name to matplotlib Figure.
    """
    figures: Dict[str, plt.Figure] = {}

    for col in numeric_cols:
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.histplot(df[col].dropna(), kde=True, ax=ax)
        ax.set_title(f"Histogram of {col}")
        ax.set_xlabel(col)
        ax.set_ylabel("Frequency")
        figures[col] = fig

    logger.info("Created %d histogram plots.", len(figures))
    return figures


def create_boxplots(df: pd.DataFrame, numeric_cols: List[str]) -> Dict[str, plt.Figure]:
    """
    Create boxplots for numeric columns.

    Returns:
        Mapping from column name to matplotlib Figure.
    """
    figures: Dict[str, plt.Figure] = {}

    for col in numeric_cols:
        fig, ax = plt.subplots(figsize=(6, 2.5))
        sns.boxplot(x=df[col].dropna(), ax=ax)
        ax.set_title(f"Boxplot of {col}")
        figures[col] = fig

    logger.info("Created %d boxplot plots.", len(figures))
    return figures


def create_correlation_heatmap(df: pd.DataFrame, numeric_cols: List[str]) -> plt.Figure | None:
    """
    Create a correlation heatmap using numeric columns.

    Returns:
        A matplotlib Figure or None if not enough numeric columns.
    """
    if len(numeric_cols) < 2:
        logger.info("Not enough numeric columns for correlation heatmap.")
        return None

    corr = df[numeric_cols].corr()

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr, annot=False, cmap="coolwarm", ax=ax)
    ax.set_title("Correlation Heatmap")

    logger.info("Created correlation heatmap.")
    return fig


def create_categorical_bars(df: pd.DataFrame, categorical_cols: List[str], top_n: int = 10) -> Dict[str, plt.Figure]:
    """
    Create bar charts for categorical variables (top N categories).

    Returns:
        Mapping from column name to matplotlib Figure.
    """
    figures: Dict[str, plt.Figure] = {}

    for col in categorical_cols:
        value_counts = df[col].value_counts().head(top_n)

        fig, ax = plt.subplots(figsize=(6, 4))
        value_counts.plot(kind="bar", ax=ax)
        ax.set_title(f"Top {top_n} categories in {col}")
        ax.set_xlabel(col)
        ax.set_ylabel("Count")
        figures[col] = fig

    logger.info("Created %d categorical bar plots.", len(figures))
    return figures

