import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.utils import PlotlyJSONEncoder
import json
from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
import numpy as np
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Create uploads folder if not exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls', 'json'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_data(filepath):
    """Load supported file types into DataFrame"""
    ext = filepath.rsplit('.', 1)[1].lower()
    if ext == 'csv':
        return pd.read_csv(filepath)
    elif ext in ['xlsx', 'xls']:
        return pd.read_excel(filepath)
    elif ext == 'json':
        return pd.read_json(filepath)
    else:
        raise ValueError("Unsupported file format")

def analyze_data(df):
    """Extract insights"""
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()

    analysis = {
        'shape': df.shape,
        'columns': list(df.columns),
        'dtypes': {k: str(v) for k, v in df.dtypes.to_dict().items()},
        'missing_values': df.isnull().sum().to_dict(),
        'numeric_columns': numeric_cols,
        'categorical_columns': categorical_cols,
        'sample_data': df.head(10).to_dict('records')
    }

    if numeric_cols:
        analysis['statistics'] = df[numeric_cols].describe().to_dict()

    return analysis

def create_visualizations(df):
    plots = {}
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    # 1. Time Series Plot
    date_cols = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()]
    sales_cols = [col for col in df.columns if any(key in col.lower() for key in ['sales', 'amount', 'revenue', 'total', 'price'])]
    
    if date_cols and sales_cols:
        try:
            df[date_cols[0]] = pd.to_datetime(df[date_cols[0]], errors='coerce')
            df = df.dropna(subset=[date_cols[0]])
            fig = px.line(df, x=date_cols[0], y=sales_cols[0], title=f"{sales_cols[0]} Over Time")
            plots['time_series'] = json.dumps(fig, cls=PlotlyJSONEncoder)
        except Exception as e:
            print("Time Series Plot Error:", e)

    # 2. Top Categories Bar Chart
    if categorical_cols and numeric_cols:
        try:
            grouped = df.groupby(categorical_cols[0])[numeric_cols[0]].sum().sort_values(ascending=False).head(10)
            fig = px.bar(x=grouped.index, y=grouped.values, 
                         title=f"Top 10 {categorical_cols[0]} by {numeric_cols[0]}",
                         labels={'x': categorical_cols[0], 'y': numeric_cols[0]})
            plots['top_categories'] = json.dumps(fig, cls=PlotlyJSONEncoder)
        except Exception as e:
            print("Top Categories Plot Error:", e)

    # 3. Histogram
    if numeric_cols:
        try:
            fig = px.histogram(df, x=numeric_cols[0], title=f"Distribution of {numeric_cols[0]}")
            plots['distribution'] = json.dumps(fig, cls=PlotlyJSONEncoder)
        except Exception as e:
            print("Histogram Error:", e)

    # 4. Correlation Heatmap
    if len(numeric_cols) > 1:
        try:
            corr = df[numeric_cols].corr()
            fig = px.imshow(corr, text_auto=True, title="Correlation Heatmap")
            plots['correlation'] = json.dumps(fig, cls=PlotlyJSONEncoder)
        except Exception as e:
            print("Correlation Heatmap Error:", e)

    # 5. Pie Chart
    if categorical_cols:
        try:
            top_cats = df[categorical_cols[0]].value_counts().head(10)
            fig = px.pie(values=top_cats.values, names=top_cats.index, 
                         title=f"Top {categorical_cols[0]} Distribution")
            plots['pie_chart'] = json.dumps(fig, cls=PlotlyJSONEncoder)
        except Exception as e:
            print("Pie Chart Error:", e)

    return plots

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files or request.files['file'].filename == '':
        flash('No file selected')
        return redirect(url_for('index'))

    file = request.files['file']
    
    if allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            df = load_data(filepath)
            analysis = analyze_data(df)
            plots = create_visualizations(df)
            os.remove(filepath)  # cleanup

            return render_template('dashboard.html', analysis=analysis, plots=plots)
        except Exception as e:
            flash(f"Error processing file: {str(e)}")
            if os.path.exists(filepath):
                os.remove(filepath)
            return redirect(url_for('index'))

    flash("Invalid file type. Only CSV, Excel, or JSON allowed.")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
