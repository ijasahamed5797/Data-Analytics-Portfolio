# 🤖 AI Auto Data Analyst

A GenAI-powered data analyst that can:

- Ingest a CSV file
- Profile and summarize the dataset
- Auto-generate visualizations (histograms, boxplots, correlation heatmaps, bar charts)
- Generate natural-language insights using Google's Gemini models
- Answer natural-language questions about the data by generating and executing pandas code

## 🧱 Project Structure

```text
AUTO_ANALYST/
│
├── pipeline/
│   ├── data_ingestion.py      # CSV loading & type inference
│   ├── profiling.py           # Dataset summary builder
│   ├── visualization.py       # Plot generation
│   ├── llm_insights.py        # Gemini EDA report
│   └── qa_agent.py            # Question → code → execution
│
├── app_streamlit.py           # Streamlit UI
├── config.py                  # Settings (API key, model)
└── README.md
