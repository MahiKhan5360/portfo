import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Home Route
@app.route('/')
def home():
    return render_template('index.html')

# Dynamic Page Route
@app.route("/<string:page_name>")
def html_page(page_name):
    return render_template(page_name)

# Route for Data Insights Generator
@app.route('/data-insights', methods=['GET', 'POST'])
def data_insights():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file uploaded", 400

        file = request.files['file']

        if file.filename == '':
            return "No file selected", 400

        if file and file.filename.endswith('.csv'):
            filepath = os.path.join('static/uploads', file.filename)
            file.save(filepath)

            df = pd.read_csv(filepath)

            # Generate insights
            insights = {
                "shape": df.shape,
                "missing_values": df.isnull().sum().to_dict(),
                "summary": df.describe().to_html(),
                "columns": df.dtypes.to_dict()
            }

            return render_template('data_insights.html', insights=insights, filename=file.filename)
    
    return render_template('data_insights.html', insights=None)


print("Flask server is running...")
app.run(debug=True)

