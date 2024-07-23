from flask import Flask, request, jsonify, render_template, send_file
import pandas as pd
import numpy as np
from credit_fraud_decision_tree import detect_fraud
import os

app = Flask(__name__)

# Directory to save processed files
PROCESSED_FILES_DIR = 'processed_files'
os.makedirs(PROCESSED_FILES_DIR, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect-fraud', methods=['POST'])
def detect_fraud_endpoint():
    data = request.json
    features = data['features']

    # Check if we have exactly 28 features
    if len(features) != 28:
        return jsonify({'message': 'Invalid number of features, should be 28'}), 400

    result = detect_fraud(features)
    return jsonify({'message': result})

@app.route('/upload-dataset', methods=['POST'])
def upload_dataset():
    if 'file' not in request.files:
        return jsonify({'message': 'No file uploaded'}), 400

    file = request.files['file']
    file_path = os.path.join(PROCESSED_FILES_DIR, 'processed_dataset.csv')

    try:
        df = pd.read_csv(file)

        # Ensure the dataset has at least 28 columns
        if df.shape[1] < 28:
            return jsonify({'message': 'Dataset should have at least 28 columns'}), 400

        # Apply fraud detection to each row of the dataset
        results = []
        for _, row in df.iterrows():
            features = row.values[:28]  # Only take the first 28 features
            result = detect_fraud(features)
            results.append(result)

        # Add results to the dataset
        df['Fraud Status'] = results
        df.to_csv(file_path, index=False)

        return jsonify({'message': 'Dataset processed successfully', 'file_url': '/download/processed_dataset.csv'})

    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(PROCESSED_FILES_DIR, filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
