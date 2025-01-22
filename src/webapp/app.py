from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import sys
import shutil
from bs4 import BeautifulSoup  # You might need to: poetry add beautifulsoup4

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
    map_path = os.path.join(app.static_folder, 'analysis/location_analysis.html')
    try:
        with open(map_path, 'r') as f:
            content = f.read()
            soup = BeautifulSoup(content, 'html.parser')
            
            # Get all CSS and JS from head
            head = soup.find('head')
            css_links = [str(link) for link in head.find_all('link')] if head else []
            head_scripts = [str(script) for script in head.find_all('script')] if head else []
            
            # Extract the initialization scripts
            init_script = soup.find('script', string=lambda t: t and 'L_NO_TOUCH = false;' in t)
            map_script = soup.find('script', string=lambda t: t and 'var map_' in t)
            
            # Get the map ID from the script
            map_id = None
            if map_script and 'var map_' in map_script.string:
                map_id = map_script.string.split('var map_')[1].split('=')[0].strip()
                print(f"Found map ID: {map_id}")
            
            # Combine scripts
            combined_script = ""
            if init_script:
                combined_script += init_script.string + "\n"
            if map_script:
                combined_script += map_script.string
            
            # Create div with correct ID
            map_div = f"<div id='map_{map_id}' style='height: 80vh;'></div>" if map_id else "<div id='map'></div>"
            
            return render_template('map.html', 
                                map_div=map_div,
                                map_script=combined_script,
                                css_links=css_links,
                                head_scripts=head_scripts)
                
    except Exception as e:
        print(f"Error processing map file: {e}")
        return render_template('map.html', 
                             map_div="<div id='map'></div>",
                             map_script="",
                             css_links=[],
                             head_scripts=[])

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