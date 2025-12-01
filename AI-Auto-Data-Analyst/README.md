# 🤖 AI Auto Data Analyst

## 📌 Project Overview
AI Auto Data Analyst is an intelligent end-to-end data exploration tool built using **Python**, **Streamlit**, **Pandas**, and **Google Gemini AI**.  
It automates manual EDA workflows by generating insights, visualizations, and Python code — all from a natural language question.

This project allows users to upload **any CSV file**, and the system automatically:
- Profiles the dataset  
- Creates smart visualizations  
- Generates analytical insights  
- Answers questions using natural language  
- Produces plots on demand (bar, line, pie, trend, etc.)  
- Executes the generated code and returns the result  

---

## 🎯 Problem Statement
Exploratory Data Analysis (EDA) is time-consuming, repetitive, and requires coding skills.  
Many business users struggle to understand data without technical support.

This tool solves that by:
- Turning English questions into Python code  
- Auto-generating visuals  
- Providing interpretable insights instantly  
- Eliminating manual analysis work  

---

## 🔄 System Pipeline (How It Works)

### **1. Data Ingestion**
- Loads any CSV uploaded by the user  
- Detects column types: numeric vs categorical  
- Handles missing/duplicate data  
- Stores the dataframe for downstream operations  

### **2. Automated EDA**
- Summary statistics  
- Outlier detection  
- Histograms & boxplots  
- Correlation heatmaps  
- Categorical distributions  

### **3. AI-powered Insights (Gemini)**
Gemini is prompted with a structured summary and produces:
- Key dataset observations  
- Trend detection  
- Outlier discussion  
- Business-ready insights  

### **4. Natural Language Query → Python Code**
User example:  
> “In which region were laptops sold the most?”

The agent:
1. Cleans the query (case-insensitive, singular/plural handling)  
2. Understands intent  
3. Generates Python code  
4. Executes the code  
5. Returns the answer  

### **5. AI Plot Generator (Using Gemini)**
User example:  
> “Create a bar chart of revenue by product”

The model returns executable code to:
- Build the visualization  
- Display the chart  
- Handle errors safely  

### **6. Streamlit Frontend**
- Smooth UI  
- Supports real-time code execution  
- Displays insights, EDA visualizations, queries, and charts  

---

## 🧩 Technologies Used

### **Backend**
- Python 3.x  
- Pandas  
- Matplotlib  
- Seaborn  

### **AI**
- Google Gemini 1.5 (Text + Code)  
- Prompt engineering for query translation & plotting  

### **Frontend**
- Streamlit  

### **DevOps / Other**
- Virtual environment  
- Requirements file  
- GitHub project structure  

---

## 🚀 Key Features

### 🔍 **Automated EDA**
- Summary metrics  
- Histograms  
- Boxplots  
- Correlation matrix  
- Category counts  

### 🧠 **AI-powered Insights**
- Gemini explains data trends  
- Highlights correlations  
- Points out interesting observations  

### 💬 **Natural Language Q&A**
Ask:
- “Which region has the highest revenue?”  
- “How many laptops were sold in the North?”  
- “Show me trend of monthly sales.”  

The system generates:
- Clean Python code  
- Executes it  
- Shows result instantly  

### 📊 **AI-Generated Visualizations**
- Bar chart  
- Line chart  
- Pie chart  
- Trend chart  
- Category comparison  

### 🔤 **Smart Query Handling**
- Case-insensitive  
- Singular/plural friendly  
- Works with ANY dataset  

---

## 📁 Project Structure

```
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
│── requirements.txt
│── README.md
│── .env (not included)
```

---

## ▶️ Run Locally

```
pip install -r requirements.txt
streamlit run app_streamlit.py
```

---

## 📌 Summary
AI Auto Data Analyst combines **automation + AI + visualization** to simplify data exploration for both analysts and non-technical users.  
It reduces analysis time, improves insights, and provides an interactive ML-powered data experience.

---

Made with ❤️ using Streamlit + Gemini  
