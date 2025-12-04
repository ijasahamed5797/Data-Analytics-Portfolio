📈 Stock Price Forecasting Project

An end-to-end Time Series Forecasting solution using multiple ML & Deep Learning models, combined with an interactive Streamlit application for real-time stock analysis and prediction.

🚀 Project Overview

This project demonstrates a complete workflow of stock market prediction — from EDA, feature engineering, and model development, to deployment of an interactive Streamlit app.

It includes:

Exploratory Data Analysis

Traditional Time Series Models

Deep Learning Forecasting Models

Comparison across multiple architectures

A real-time Streamlit dashboard

Automated email alerts for stock price thresholds

This project replaces my earlier Apple Stock Analysis project and serves as a full portfolio-grade demonstration of time-series modeling.

🧠 Models Implemented

This repository includes notebooks for multiple forecasting approaches:

📌 Statistical Models

ARIMA / SARIMA

Prophet (Facebook Prophet)

📌 Deep Learning Models

LSTM (Single-layer & Multi-layer)

GRU Model

CNN-LSTM Hybrid Model

📌 Benchmark

Naïve Forecast

Moving Average Forecast

Each notebook includes training, evaluation, visualization, and forecasting.

🧪 Notebooks Included
Notebook	Description
01_data_eda.ipynb	Data collection + exploratory data analysis
02_arima_modelling.ipynb	ARIMA model tuning & forecasting
03_lstm_modelling.ipynb	LSTM forecasting model
04_multistock_comparison.ipynb	Compare predictions across several tickers
05_prophet_model.ipynb	Prophet forecasting
06_cnn_lstm_modelling.ipynb	CNN + LSTM hybrid neural network
07_gru_modelling.ipynb	GRU model for forecasting

All notebooks are organized inside the notebooks/ folder.

🖥️ Streamlit Application

The app/ folder contains a fully functional Streamlit dashboard that includes:

✔ Downloading real-time stock data from Yahoo Finance
✔ Interactive price visualizations
✔ Model-driven forecasting
✔ Email alert system for price triggers
✔ Clean UI for user interaction

To run the app locally:
```
cd app
pip install -r requirements.txt
streamlit run app.py
```

📁 Project Folder Structure

```
stock-price-forecasting/
│
├── app/
│   ├── app.py
│   ├── email_alert.py
│   ├── requirements.txt
│   └── .gitignore
│
├── notebooks/
│   ├── 01_data_eda.ipynb
│   ├── 02_arima_modelling.ipynb
│   ├── 03_lstm_modelling.ipynb
│   ├── 04_multistock_comparison.ipynb
│   ├── 05_prophet_model.ipynb
│   ├── 06_cnn_lstm_modelling.ipynb
│   ├── 07_gru_modelling.ipynb
│
│
└── README.md
```

📦 Installation

Clone the repository:
```
git clone https://github.com/ijasahamed5797/Data-Science-Portfolio.git
cd stock-price-forecasting
```
Install dependencies for the Streamlit app:
```
pip install -r app/requirements.txt
```

📊 Forecast Examples



📬 Email Alert System

The project includes an optional script (email_alert.py) that sends automated notifications when a stock crosses a price threshold.

You can integrate it directly into the Streamlit app or run it as a standalone background script.

🌟 Future Improvements

Add hyperparameter tuning via Optuna

Deploy Streamlit app to Streamlit Cloud

Add ensemble forecasting

Integrate sentiment analysis from financial news

Add Docker support

📝 Conclusion

This project provides a complete, end-to-end demonstration of:

Data engineering

Classical and modern time-series modeling

Neural networks for forecasting

Interactive application deployment

It highlights practical Data Science skills applied to real-world forecasting problems.
