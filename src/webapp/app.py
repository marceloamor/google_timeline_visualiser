from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import sys
import shutil
from bs4 import BeautifulSoup
import folium
import re
import traceback

# Add parent directory to path to access existing modules
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from data_extraction import extract_timeline_data
from temporal_analysis import analyze_temporal_patterns
from geoanalysis import analyze_locations

app = Flask(__name__)

# Ensure static directories exist
os.makedirs(os.path.join(app.static_folder, 'analysis'), exist_ok=True)

def update_analysis_files():
    """Run analysis and copy output files to static folder"""
    # Run analysis if needed
    if not os.path.exists('output/location_analysis.html'):
        extract_timeline_data()
        analyze_temporal_patterns()
        analyze_locations()
    
    # Copy analysis files to static folder
    shutil.copy('output/location_analysis.html', 
                os.path.join(app.static_folder, 'analysis/location_analysis.html'))
    shutil.copy('output/temporal_patterns.png',
                os.path.join(app.static_folder, 'analysis/temporal_patterns.png'))
    shutil.copy('output/location_statistics.json',
                os.path.join(app.static_folder, 'analysis/location_statistics.json'))
    shutil.copy('output/temporal_statistics.json',
                os.path.join(app.static_folder, 'analysis/temporal_statistics.json'))

@app.route('/')
def index():
    update_analysis_files()
    return render_template('index.html')

@app.route('/map')
def map_view():
    update_analysis_files()
    
    # Create a new map instance
    m = folium.Map(location=[0, 0], zoom_start=2)
    
    # Read the original map file to get the layers
    map_path = os.path.join(app.static_folder, 'analysis/location_analysis.html')
    try:
        with open(map_path, 'r') as f:
            content = f.read()
            soup = BeautifulSoup(content, 'html.parser')
            
            # Extract marker data instead of scripts
            markers = []
            scripts = soup.find_all('script')
            for script in scripts:
                if not script.string:
                    continue
                    
                if 'circle_marker_' in script.string:
                    # Extract marker data using regex
                    coords_match = re.search(r'L\.circleMarker\(\s*\[([-\d.]+),\s*([-\d.]+)\]', script.string)
                    # Capture the entire options object
                    options_match = re.search(r'{\s*"[^}]+":\s*[^}]+(?:,\s*"[^}]+":\s*[^}]+)*}', script.string)
                    # Capture the entire popup HTML content
                    popup_match = re.search(r'\$\(`<div[^>]*>(.*?)</div>`\)', script.string, re.DOTALL)
                    
                    if coords_match and options_match:
                        markers.append({
                            'lat': float(coords_match.group(1)),
                            'lng': float(coords_match.group(2)),
                            'options': options_match.group(0),  # Use the full options object
                            'popup': popup_match.group(1).strip() if popup_match else ''
                        })
            
            print(f"Extracted {len(markers)} markers")  # Debug info
            
            return render_template('map.html', 
                                map=m.get_root().render(),
                                markers=markers)
                
    except Exception as e:
        print(f"Error processing map file: {e}")
        traceback.print_exc()  # Print full stack trace
        return render_template('map.html', 
                             map=m.get_root().render(),
                             markers=[])

@app.route('/temporal')
def temporal_view():
    update_analysis_files()
    return render_template('temporal.html')

@app.route('/statistics')
def statistics_view():
    update_analysis_files()
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