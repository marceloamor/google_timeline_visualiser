import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from icecream import ic
import json
from googlemaps import Client
import collections
import time
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment variable
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

def extract_timeline_data(input_file='data/Timeline.json'):
    """Extract both visits and activities from Timeline.json"""
    
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    visits = []
    activities = []
    
    for segment in data.get('semanticSegments', []):
        # Common time data
        time_data = {
            'start_time': segment.get('startTime'),
            'end_time': segment.get('endTime'),
            'timezone_offset': segment.get('startTimeTimezoneUtcOffsetMinutes')
        }
        
        if 'visit' in segment:
            visit = segment['visit']
            top_candidate = visit.get('topCandidate', {})
            
            visit_data = {
                **time_data,
                'place_id': top_candidate.get('placeId'),
                'semantic_type': top_candidate.get('semanticType'),
                'probability': visit.get('probability'),
                'hierarchy_level': visit.get('hierarchyLevel'),
                'location': top_candidate.get('placeLocation', {}).get('latLng')
            }
            visits.append(visit_data)
            
        elif 'activity' in segment:
            activity = segment['activity']
            top_candidate = activity.get('topCandidate', {})
            
            activity_data = {
                **time_data,
                'type': top_candidate.get('type'),
                'probability': top_candidate.get('probability'),
                'distance_meters': activity.get('distanceMeters'),
                'start_location': activity.get('start', {}).get('latLng'),
                'end_location': activity.get('end', {}).get('latLng')
            }
            activities.append(activity_data)
    
    # Save extracted data
    extracted_data = {
        'metadata': {
            'total_segments': len(data.get('semanticSegments', [])),
            'total_visits': len(visits),
            'total_activities': len(activities),
            'extraction_date': datetime.now().isoformat()
        },
        'visits': visits,
        'activities': activities
    }
    
    with open('data/extracted_timeline.json', 'w') as f:
        json.dump(extracted_data, f, indent=2)
    
    ic(f"Extracted {len(visits)} visits and {len(activities)} activities")
    return extracted_data

if __name__ == "__main__":
    extract_timeline_data()