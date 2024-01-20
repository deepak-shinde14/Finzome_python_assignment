import os
import pandas as pd
from flask import Flask, jsonify, request, abort
import numpy as np

app = Flask(__name__)

CSV_DIRECTORY = "C:/Users/shind/Downloads/"

def load_data(file):
    """
    Load data from a CSV file.

    Parameters:
    - file (FileStorage): The uploaded CSV file.

    Returns:
    - pd.DataFrame: The loaded data.
    """
    try:
        data = pd.read_csv(file)
        # Validate that 'Close' column is present
        if 'Close ' not in data.columns:
            raise ValueError("Missing 'Close' column in CSV file")
        return data
    except pd.errors.EmptyDataError:
        abort(400, {'error': 'Empty CSV file'})
    except pd.errors.ParserError:
        abort(400, {'error': 'Invalid CSV file format'})

def compute_volatility(data):
    """
    Compute daily and annualized volatility.

    Parameters:
    - data (pd.DataFrame): The DataFrame containing financial data.

    Returns:
    - Tuple[float, float]: Daily and annualized volatility.
    """
    # Assuming the CSV file has a column named 'Close' for daily closing prices
    close_prices = data['Close ']

    # Calculate Daily Returns
    data['Daily Returns'] = (close_prices / close_prices.shift(1)) - 1

    # Calculate Daily Volatility
    daily_volatility = np.std(data['Daily Returns'])

    # Calculate Annualized Volatility
    annualized_volatility = daily_volatility * np.sqrt(len(data))

    return daily_volatility, annualized_volatility

@app.route('/compute_volatility', methods=['POST', 'GET'])
def compute_volatility_endpoint():
    """
    Endpoint to compute daily and annualized volatility.

    POST Method Parameters:
    - file (file): The uploaded CSV file.

    GET Method Parameters:
    - filename (str): The name of the CSV file.

    Returns:
    - JSON: Result containing daily and annualized volatility.
    """
    if request.method == 'POST':
        if 'file' not in request.files:
            abort(400, {'error': 'No file provided'})

        file = request.files['file']
        if file.filename == '':
            abort(400, {'error': 'Empty file name'})

        # Validate file extension
        if not file.filename.endswith('.csv'):
            abort(400, {'error': 'Invalid file format. Must be a CSV file'})

        data = load_data(file)

    elif request.method == 'GET':
        filename = request.args.get('filename')
        if not filename:
            abort(400, {'error': 'Please provide a filename parameter'})

        csv_path = os.path.join(CSV_DIRECTORY, filename)

        # Check if the file exists
        if not os.path.exists(csv_path):
            abort(404, {'error': 'File not found'})

        data = pd.read_csv(csv_path)

    else:
        abort(400, {'error': 'Invalid request method. Use POST to upload a file or GET with a filename parameter.'})

    daily_volatility, annualized_volatility = compute_volatility(data)

    result = {
        'daily_volatility': daily_volatility,
        'annualized_volatility': annualized_volatility
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)


