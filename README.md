# Data Analysis Tool API

This project is a web-based data analysis tool that allows users to:
1. Upload CSV or Excel files.
2. Create visualizations with selected columns on x and y axes.
3. Generate a PDF summary with insights on the dataset.

## Features
- **File Upload**: Uploads CSV or Excel files for analysis.
- **Data Visualization**: Select multiple columns for x and y axes; supports scatter, line, and bar plots.
- **Summary Generation**: Generates a PDF summary with insights based on the dataset’s statistical data.

## Requirements
- **Python 3.7+**
- Packages in `requirements.txt` (Flask, pandas, plotly, transformers, fpdf, kaleido)

## Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/data_analysis_tool.git
   cd data_analysis_tool
Create and Activate Virtual Environment:

bash
Copy code
python -m venv venv
On Windows: .\venv\Scripts\activate
On macOS/Linux: source venv/bin/activate
Install Dependencies:

bash
Copy code
pip install -r requirements.txt
Run the Application:

bash
Copy code
python app.py
Access the Application: Open http://127.0.0.1:5000 in your browser.

Usage
Upload Files: Use the upload form to load your CSV or Excel file.
Create Visualizations: Select columns for x and y axes, choose the type of plot, and generate visualizations.
Generate Summary: Get a PDF summary of dataset statistics and insights.

License
This code is for personal or educational use only and is not licensed for commercial distribution or modification without permission.

Contact
For questions, contact production23@live.com
