# Data Analysis Tool API

This project provides a web-based data analysis tool that allows users to:
1. Upload data files (CSV or Excel).
2. Generate visualizations with selectable columns for both x and y axes.
3. Generate a PDF summary of statistical insights from the dataset.

## Features
- **File Upload**: Uploads CSV or Excel files for analysis.
- **Data Visualization**: Allows multi-column selection for x and y axes, supporting scatter, line, and bar plots.
- **Summary Generation**: Uses a T5 language model to generate a PDF summary of statistical insights based on descriptive statistics.

## Requirements
- **Python 3.7+**
- **Packages**:
  - Flask
  - pandas
  - plotly
  - transformers
  - fpdf
  - tempfile
  - kaleido (for saving Plotly images)

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/data_analysis_tool.git
   cd data_analysis_tool
Install Dependencies: Install the required Python packages:

bash
Copy code
pip install -r requirements.txt
Download the T5 Model: The application uses the Hugging Face T5 model (t5-small) for generating summaries. The model is downloaded automatically if not already present.

Run the Application: Start the Flask server:

bash
Copy code
python app.py
The application should now be running on http://127.0.0.1:5000.

Access the Application: Open your web browser and go to http://127.0.0.1:5000.

Usage
File Upload:

Use the Upload File form to upload a CSV or Excel file. Once uploaded, the column titles are extracted and displayed for further analysis.
Generate Visualizations:

Select the columns for the x and y axes, and choose a visualization type (scatter, line, or bar plot).
Click Generate Visualization to create the plot. The generated visualizations will be displayed on the main page.
Generate Summary:

The Generate Summary section allows you to create a PDF analysis of your dataset.
This summary uses the T5 model to provide insights based on the descriptive statistics of the data.

File Structure
app.py: Main application file that includes all routes and the Flask application logic.
static/temp_images/: Directory where generated visualizations are temporarily stored.
data_analysis_tool/models/t5_model/: Directory where the T5 model is saved locally after download.

Customization
Modify Visualization Types: You can add or remove supported visualization types in the /visualize route of app.py.
Refine Summary Prompt: Update the prompt in the /summary route to adjust how the T5 model summarizes your data.

Troubleshooting
Model Download Issues: Ensure internet connectivity for the initial download of the T5 model.
Permission Errors: If encountering permission issues with temp files, ensure sufficient permissions in the working directory.
Large Session Cookie Warning: The app has been modified to prevent large session cookies by storing images on the server instead of in the session.

License
None

Contact
For any questions or feedback, please contact production23@live.com
