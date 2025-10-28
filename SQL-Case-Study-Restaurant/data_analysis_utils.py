"""
Data Analysis Utilities
Supporting functions for data analytics projects
"""

import pandas as pd
import numpy as np

def analyze_sales_data(df):
    """
    Analyze sales data and return key metrics
    """
    analysis = {
        'total_customers': df['customer_id'].nunique(),
        'total_orders': len(df),
        'date_range': {
            'start': df['order_date'].min(),
            'end': df['order_date'].max()
        },
        'average_order_value': df.groupby('order_date')['price'].sum().mean()
    }
    return analysis

def calculate_customer_metrics(df):
    """
    Calculate customer-level metrics
    """
    customer_stats = df.groupby('customer_id').agg({
        'order_date': ['count', 'nunique'],
        'price': ['sum', 'mean']
    }).round(2)
    
    customer_stats.columns = ['total_orders', 'visit_days', 'total_spent', 'avg_spend']
    return customer_stats

def generate_sales_report(df):
    """
    Generate comprehensive sales report
    """
    report = {
        'summary': analyze_sales_data(df),
        'customer_metrics': calculate_customer_metrics(df),
        'top_products': df['product_name'].value_counts().head(5)
    }
    return report

if __name__ == "__main__":
    print("Data Analytics Utilities Loaded")
