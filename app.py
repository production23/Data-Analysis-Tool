from flask import Flask, request, jsonify, send_file, render_template_string, redirect, url_for, session
import pandas as pd
import plotly.express as px
import os
import tempfile
from transformers import T5ForConditionalGeneration, T5Tokenizer
from fpdf import FPDF
import glob
import re

# Define the directory for the model
model_directory = "data_analysis_tool/models/t5_model"

# Load or save the T5 model and tokenizer if not already saved locally
if not os.path.exists(model_directory):
    model = T5ForConditionalGeneration.from_pretrained('t5-small')
    tokenizer = T5Tokenizer.from_pretrained('t5-small')
    model.save_pretrained(model_directory)
    tokenizer.save_pretrained(model_directory)
else:
    model = T5ForConditionalGeneration.from_pretrained(model_directory)
    tokenizer = T5Tokenizer.from_pretrained(model_directory)

# Create the Flask app instance
app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for session management

# HTML template with forms for each endpoint
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Data Analysis Tool API</title>
</head>
<body>
    <h1>Data Analysis Tool API</h1>
    <p>Use the forms below to upload files, generate visualizations, and create summaries.</p>

    <h2>Upload File</h2>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="file">
        <button type="submit">Upload</button>
    </form>

    {% if file_uploaded %}
    <p style="color: green;">File uploaded successfully! Now you can select columns for visualization.</p>
    {% endif %}

    {% if columns %}
    <h2>Select Columns for Visualization</h2>
    <form action="/visualize" method="post">
        <label>X Columns:</label><br>
        {% for col in columns %}
            <input type="checkbox" name="x_column" value="{{ col }}"> {{ col }}<br>
        {% endfor %}

        <label>Y Columns:</label><br>
        {% for col in columns %}
            <input type="checkbox" name="y_column" value="{{ col }}"> {{ col }}<br>
        {% endfor %}

        <label for="viz_type">Visualization Type:</label>
        <select name="viz_type" required>
            <option value="scatter">Scatter</option>
            <option value="line">Line</option>
            <option value="bar">Bar</option>
        </select><br>
        <button type="submit">Generate Visualization</button>
    </form>
    {% endif %}

    <h2>Generate Summary</h2>
    <form action="/summary" method="post">
        <label for="file">File Path:</label>
        <input type="text" name="file" placeholder="Path to your file" required><br>
        <button type="submit">Generate Summary</button>
    </form>

    {% if images %}
    <h2>Generated Visualizations</h2>
    {% for img in images %}
        <img src="{{ img }}" alt="Visualization" style="display: block; margin: 10px 0;">
    {% endfor %}
    {% endif %}
</body>
</html>
"""

@app.route('/')
def home():
    columns = session.get("columns")
    file_uploaded = session.get("file_uploaded", False)

    # List all generated image files in the temp directory for display
    image_files = glob.glob("static/temp_images/*.png")
    images = [f"/{img}" for img in image_files]  # Prepare paths for HTML display

    return render_template_string(html_template, columns=columns, file_uploaded=file_uploaded, images=images)

@app.route('/upload', methods=['POST'])
def upload_file():
    session.pop("columns", None)
    session.pop("file_path", None)
    session["file_uploaded"] = False

    file = request.files['file']
    if not file:
        return jsonify({"error": "No file provided"}), 400
    
    # Save file temporarily
    temp_file_path = tempfile.NamedTemporaryFile(delete=False, suffix=".csv" if file.filename.endswith('.csv') else ".xlsx").name
    file.save(temp_file_path)

    # Read file into DataFrame and retrieve columns
    df = pd.read_csv(temp_file_path) if file.filename.endswith('.csv') else pd.read_excel(temp_file_path)
    columns = df.columns.tolist()
    
    session["columns"] = columns
    session["file_path"] = temp_file_path
    session["file_uploaded"] = True
    return redirect(url_for('home'))

@app.route('/visualize', methods=['POST'])
def visualize_data():
    x_columns = request.form.getlist('x_column')
    y_columns = request.form.getlist('y_column')
    viz_type = request.form['viz_type']
    file_path = session.get("file_path")

    df = pd.read_csv(file_path) if file_path.endswith('.csv') else pd.read_excel(file_path)
    
    # Create a static directory for images
    os.makedirs("static/temp_images", exist_ok=True)

    # Clear any existing images in the temp directory
    for file in glob.glob("static/temp_images/*.png"):
        os.remove(file)
    
    images = []
    for x_column in x_columns:
        for y_column in y_columns:
            fig = None
            if viz_type == 'scatter':
                fig = px.scatter(df, x=x_column, y=y_column)
            elif viz_type == 'line':
                fig = px.line(df, x=x_column, y=y_column)
            elif viz_type == 'bar':
                fig = px.bar(df, x=x_column, y=y_column)

            if fig:
                # Sanitize file names by replacing non-alphanumeric characters with underscores
                safe_x_column = re.sub(r'\W+', '_', x_column)
                safe_y_column = re.sub(r'\W+', '_', y_column)
                
                # Save image to the static directory
                image_path = f"static/temp_images/{viz_type}_{safe_x_column}_vs_{safe_y_column}.png"
                fig.write_image(image_path)
                images.append(image_path)

    return redirect(url_for('home'))

@app.route('/summary', methods=['POST'])
def generate_summary():
    file_path = session.get("file_path")
    df = pd.read_csv(file_path) if file_path.endswith('.csv') else pd.read_excel(file_path)

    # Refined prompt for more insightful summary
    input_text = f"Analyze and explain what the following data summary means in simple terms:\n{df.describe().to_string()}"
    input_ids = tokenizer.encode(input_text, return_tensors='pt')
    
    # Generate summary using the T5 model
    summary_ids = model.generate(input_ids, max_length=150, num_beams=2, early_stopping=True)
    summary_text = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    # Save the summary as a PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, summary_text)
    pdf_output = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(pdf_output.name)
    
    return send_file(pdf_output.name, mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)
