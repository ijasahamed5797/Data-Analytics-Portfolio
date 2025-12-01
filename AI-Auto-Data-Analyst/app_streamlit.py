"""
Streamlit frontend for the Auto Analyst project.
"""

from __future__ import annotations

import logging

import pandas as pd
import streamlit as st
from matplotlib.figure import Figure  # for isinstance checks

from config import settings
from pipeline.data_ingestion import infer_column_types
from pipeline.profiling import build_summary
from pipeline.visualization import (
    create_histograms,
    create_boxplots,
    create_correlation_heatmap,
    create_categorical_bars,
)
from pipeline.llm_insights import init_gemini, generate_insights
from pipeline.qa_agent import init_qa_model, run_data_query
from pipeline.plot_agent import init_plot_model, run_plot_query  # NEW


# ---------------- Logging ----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)


# ---------------- Streamlit Config ----------------
st.set_page_config(
    page_title="AI Auto Data Analyst",
    layout="wide",
)

st.title("🤖 AI Auto Data Analyst")
st.markdown(
    "Upload a CSV file and let the AI automatically explore, visualize, and "
    "answer questions about your dataset."
)

# Initialize models lazily (only when needed)
_gemini_insights_model = None
_gemini_qa_model = None
_gemini_plot_model = None  # NEW


def get_insights_model():
    global _gemini_insights_model
    if _gemini_insights_model is None:
        _gemini_insights_model = init_gemini(settings)
    return _gemini_insights_model


def get_qa_model():
    global _gemini_qa_model
    if _gemini_qa_model is None:
        _gemini_qa_model = init_qa_model(settings)
    return _gemini_qa_model


def get_plot_model():
    """Lazy init for the visualization Gemini model."""
    global _gemini_plot_model
    if _gemini_plot_model is None:
        _gemini_plot_model = init_plot_model(settings)
    return _gemini_plot_model


# ---------------- Sidebar ----------------
st.sidebar.header("Settings")
st.sidebar.write(f"Model: `{settings.gemini_model_name}`")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if not uploaded_file:
    st.info("👆 Upload a CSV file to begin.")
    st.stop()

# ---------------- Load Data ----------------
try:
    df = pd.read_csv(uploaded_file)
except Exception as exc:  # noqa: BLE001
    st.error(f"Failed to read CSV: {exc}")
    st.stop()

st.subheader("📄 Dataset Preview")
st.dataframe(df.head(), use_container_width=True)

numeric_cols, categorical_cols = infer_column_types(df)

# ---------------- Summary ----------------
st.subheader("📊 Dataset Summary")
summary = build_summary(df)
st.json(summary)

# ---------------- Auto Visualizations ----------------
st.subheader("📈 Auto Visualizations")

hist_figs = create_histograms(df, numeric_cols)
box_figs = create_boxplots(df, numeric_cols)
corr_fig = create_correlation_heatmap(df, numeric_cols)
cat_figs = create_categorical_bars(df, categorical_cols)

with st.expander("Numeric Distributions (Histograms)", expanded=True):
    if hist_figs:
        for col, fig in hist_figs.items():
            st.pyplot(fig, use_container_width=True)
    else:
        st.write("No numeric columns available.")

with st.expander("Outliers (Boxplots)"):
    if box_figs:
        for col, fig in box_figs.items():
            st.pyplot(fig, use_container_width=True)
    else:
        st.write("No numeric columns available.")

with st.expander("Correlation Heatmap"):
    if corr_fig:
        st.pyplot(corr_fig, use_container_width=True)
    else:
        st.write("Not enough numeric columns to compute correlations.")

with st.expander("Categorical Distributions (Bar Charts)"):
    if cat_figs:
        for col, fig in cat_figs.items():
            st.pyplot(fig, use_container_width=True)
    else:
        st.write("No categorical columns available.")

# ---------------- AI Insights ----------------
st.subheader("🧠 AI-Generated Insights")

if st.button("Generate AI Insights"):
    with st.spinner("Asking Gemini for insights..."):
        model = get_insights_model()
        insights_text = generate_insights(model, summary)
        st.markdown(insights_text)

# ---------------- Q&A Agent ----------------
st.subheader("💬 Ask Questions About Your Data")

question = st.text_input(
    "Ask a data question (e.g., 'Which region has the highest revenue?')"
)

if st.button("Run Query") and question:
    with st.spinner("Thinking and executing on your data..."):
        qa_model = get_qa_model()
        code, result = run_data_query(qa_model, question, df)

    st.markdown("**🔍 AI-Generated Code:**")
    st.code(code, language="python")

    st.markdown("**✅ Result:**")
    st.write(result)

# ---------------- Visual Q&A (Charts) ----------------
st.subheader("📊 Ask for Visualizations")

st.markdown(
    "Describe the chart you want. For example:\n"
    "- `Bar chart of total revenue by region`\n"
    "- `Line chart of units_sold over date for laptops`\n"
    "- `Boxplot of revenue by region`"
)

viz_question = st.text_input(
    "Describe a chart to generate:",
    key="viz_question",
)

if st.button("Generate Chart", key="viz_button") and viz_question.strip():
    with st.spinner("Asking Gemini to design your chart..."):
        plot_model = get_plot_model()
        plot_code, plot_result = run_plot_query(plot_model, viz_question, df)

    st.markdown("**🧠 AI-Generated Plot Code:**")
    st.code(plot_code, language="python")

    st.markdown("**📈 Chart:**")
    if isinstance(plot_result, Figure):
        st.pyplot(plot_result, use_container_width=True)
    elif isinstance(plot_result, list) and all(
        isinstance(f, Figure) for f in plot_result
    ):
        for fig in plot_result:
            st.pyplot(fig, use_container_width=True)
    else:
        # Either an error string or explanatory message
        st.write(plot_result)

st.markdown("---")
st.caption("Made with ❤️ using Streamlit + Gemini + pandas")
