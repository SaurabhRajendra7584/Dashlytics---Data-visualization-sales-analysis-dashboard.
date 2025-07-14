# Dashlytics - Sales Data Analytics Dashboard

A Flask-based web application for analyzing sales data and creating interactive dashboards. Upload CSV, Excel, or JSON files and get instant insights with beautiful visualizations.

## Features

- **Multi-format Support**: Upload CSV, Excel (.xlsx, .xls), or JSON files
- **Automatic Analysis**: Intelligent data analysis and visualization generation
- **Interactive Dashboards**: Beautiful, responsive charts using Plotly.js
- **Data Insights**: Statistical summaries, correlation analysis, and data quality metrics
- **Modern UI**: Clean, professional interface with Bootstrap styling

## Quick Start

### Installation

1. Navigate to the project directory:
```bash
cd Dashlytics
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On macOS/Linux
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

1. Start the Flask development server:
```bash
python app.py
```

2. Open your browser and go to: `http://localhost:5000`

3. Upload your sales data file and enjoy the dashboard!

## Supported File Formats

- **CSV**: Comma-separated values files
- **Excel**: .xlsx and .xls files
- **JSON**: JavaScript Object Notation files

## Sample Data

A sample CSV file (`sample_sales_data.csv`) is included for testing the application.

## Generated Visualizations

The application automatically generates various types of charts based on your data:

- **Time Series**: Sales/revenue trends over time
- **Bar Charts**: Top products, categories, or regions
- **Pie Charts**: Distribution of categorical data
- **Histograms**: Distribution of numerical values
- **Correlation Matrix**: Relationships between numerical variables

## Data Analysis Features

- **Basic Statistics**: Mean, standard deviation, min/max values
- **Data Quality**: Missing value detection and reporting
- **Column Information**: Data types and structure analysis
- **Sample Preview**: First 10 rows of your data

## Security Features

- File type validation
- Secure filename handling
- File size limits (16MB max)
- Temporary file cleanup

## Requirements

- Python 3.7+
- Flask 2.3.3
- pandas 2.1.0
- plotly 5.15.0
- openpyxl 3.1.2
- xlrd 2.0.1
- numpy 1.24.3

## Project Structure

```
Dashlytics/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── sample_sales_data.csv  # Sample data for testing
├── templates/
│   ├── base.html         # Base template
│   ├── index.html        # Upload page
│   └── dashboard.html    # Dashboard display
└── uploads/              # Temporary file storage (auto-created)
```

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the [MIT License](LICENSE).
