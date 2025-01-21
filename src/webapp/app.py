from flask import Flask, render_template, request, jsonify
import os
import sys

# Add parent directory to path to access existing modules
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from data_extraction import extract_timeline_data
from temporal_analysis import analyze_temporal_patterns
from geoanalysis import analyze_locations

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/map')
def map_view():
    return render_template('map.html')

@app.route('/temporal')
def temporal_view():
    return render_template('temporal.html')

@app.route('/statistics')
def statistics_view():
    return render_template('statistics.html')

@app.route('/api/process-timeline', methods=['POST'])
def process_timeline():
    """API endpoint for processing uploaded Timeline.json"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    # Handle file upload and processing
    # This will be implemented later
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True) 