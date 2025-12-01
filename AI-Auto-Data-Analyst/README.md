# 🤖 AI Auto Data Analyst

An AI-powered data analysis tool built using **Streamlit + Gemini + Pandas**.  
Upload any CSV and the AI automatically:

- Profiles your dataset  
- Generates charts on request  
- Creates insights using Gemini  
- Answers questions about your data  
- Converts natural language → executable pandas code  
- Handles case-insensitive and plural/singular queries  

---

## 🚀 Features

### 🔍 Automated EDA
- Dataset summary  
- Numeric & categorical column detection  
- Histograms, boxplots, bar charts  
- Correlation heatmap  

### 🧠 AI Insights (Gemini)
- Auto-generated written insights  
- Smart suggestions  
- Pattern detection  

### 💬 Natural Language Data Queries
Ask:
> "Which region sold the most laptops?"  
> "Plot revenue trend by month"  

The system generates:
- The pandas code  
- Executes it safely  
- Returns the answer + chart  

### 📊 AI Chart Generation
Ask for:
- Line chart  
- Bar chart  
- Pie chart  
- Trend graph  
- Category comparison  
And the agent builds the code + plot.

---

## 📁 Project Structure

AI-Auto-Data-Analyst/
│── app_streamlit.py
│── config.py
│── pipeline/
│ ├── data_ingestion.py
│ ├── profiling.py
│ ├── visualization.py
│ ├── llm_insights.py
│ ├── qa_agent.py
│ ├── plot_agent.py
│── .env (not included)
│── requirements.txt
│── README.md


---

## ▶️ Run Locally

```bash
pip install -r requirements.txt
streamlit run app_streamlit.py

Made with ❤️ using Streamlit + Gemini

4. Scroll down → **Commit new file**

Your new project folder will appear.

---

# ✅ STEP 2 — Upload Your Project Files

Now add all your files inside:

AI-Auto-Data-Analyst/

Specifically upload:

- `app_streamlit.py`
- `config.py`
- `pipeline/` folder
- `requirements.txt`

Do it by:

📁 Open folder → **Add file → Upload files**

Upload everything except `.env`.

---

# ✅ STEP 3 — Update the MAIN README (Home Page)

Open the main `README.md` in root of repo:

👉 https://github.com/ijasahamed5797/Data-Science-Portfolio/blob/main/README.md

Click **Edit**, then under “Projects” add this block:

```markdown
### 🤖 AI Auto Data Analyst
**Tools:** Python, Pandas, Streamlit, Matplotlib, Seaborn, Google Gemini API  
**Description:** An AI-powered tool that performs automated EDA, generates insights, produces visualizations on demand, and answers natural-language questions about uploaded CSV datasets.

**Key Features:**
- Auto EDA (summary, histograms, correlations, outliers)
- AI-powered insights via Gemini
- Natural language to pandas query execution
- AI-based chart creation (line, bar, pie, trend, category)
- Case-insensitive and plural/singular query handling

[View Project](./AI-Auto-Data-Analyst)
