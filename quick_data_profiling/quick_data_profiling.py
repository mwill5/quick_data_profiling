#!/usr/bin/env python3
# quick_data_profiling.py

"""
Quick Data Profiling Tool
Author: Myles Williams
Date: 10/23/2024

This tool generates a comprehensive HTML report of your dataset,
including statistical summaries, visualizations, and data quality checks.

Usage:
    python quick_data_profiling.py <data_file>
"""

import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from jinja2 import Environment, FileSystemLoader
import base64
from io import BytesIO

# Set Seaborn style
sns.set(style="whitegrid")

def load_data(file_path):
    try:
        print(f"Loading data from {file_path}...")
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file_path)
        else:
            print("Unsupported file format. Please provide a CSV or Excel file.")
            sys.exit(1)
        print("Data loaded successfully.\n")
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        sys.exit(1)

def generate_report(df, report_file='report.html'):
    # Create a directory to store images
    if not os.path.exists('images'):
        os.makedirs('images')

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

    # Generate plots and save as images
    images = {}

    # Histograms for numeric columns
    histograms = []
    for col in numeric_cols:
        plt.figure(figsize=(6, 4))
        sns.histplot(df[col].dropna(), kde=True)
        plt.title(f'Distribution of {col}')
        plt.tight_layout()
        img_path = f'images/hist_{col}.png'
        plt.savefig(img_path)
        plt.close()
        histograms.append(img_path)

    # Bar plots for categorical columns
    bar_charts = []
    for col in categorical_cols:
        plt.figure(figsize=(8, 6))
        sns.countplot(y=col, data=df, order=df[col].value_counts().index)
        plt.title(f'Count of {col}')
        plt.tight_layout()
        img_path = f'images/bar_{col}.png'
        plt.savefig(img_path)
        plt.close()
        bar_charts.append(img_path)

    # Correlation matrix
    if len(numeric_cols) >= 2:
        corr = df[numeric_cols].corr()
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr, annot=True, cmap='coolwarm')
        plt.title('Correlation Matrix')
        plt.tight_layout()
        corr_img = 'images/correlation_matrix.png'
        plt.savefig(corr_img)
        plt.close()
    else:
        corr_img = None

    # Missing values heatmap
    plt.figure(figsize=(12, 6))
    sns.heatmap(df.isnull(), cbar=False)
    plt.title('Missing Values Heatmap')
    plt.tight_layout()
    missing_img = 'images/missing_values.png'
    plt.savefig(missing_img)
    plt.close()

    # Encode images in base64
    def encode_image(img_path):
        with open(img_path, 'rb') as img_file:
            img_bytes = img_file.read()
            encoded = base64.b64encode(img_bytes).decode('utf-8')
        return encoded

    encoded_images = {}
    for img_path in histograms + bar_charts:
        img_name = os.path.basename(img_path)
        encoded_images[img_name] = encode_image(img_path)

    if corr_img:
        encoded_images['correlation_matrix.png'] = encode_image(corr_img)
    encoded_images['missing_values.png'] = encode_image(missing_img)

    # Prepare data for the report
    report_data = {
        'numeric_columns': numeric_cols,
        'categorical_columns': categorical_cols,
        'head': df.head().to_html(classes='table table-striped'),
        'describe': df.describe().to_html(classes='table table-striped'),
        'dtypes': df.dtypes.to_frame('Data Type').to_html(classes='table table-striped'),
        'missing_values': df.isnull().sum().to_frame('Missing Values').to_html(classes='table table-striped'),
        'histograms': histograms,
        'bar_charts': bar_charts,
        'encoded_images': encoded_images,
        'corr_img': 'correlation_matrix.png' if corr_img else None,
        'missing_img': 'missing_values.png',
    }

    # Load Jinja2 template
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('report_template.html')

    # Render HTML report
    html_out = template.render(report_data)
    with open(report_file, 'w') as f:
        f.write(html_out)

    print(f"Report generated: {report_file}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python quick_data_profiling.py <data_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    df = load_data(file_path)
    generate_report(df)

if __name__ == "__main__":
    main()
