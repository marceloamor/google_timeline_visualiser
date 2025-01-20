import json
import numpy as np
import folium
from folium import plugins
import matplotlib.pyplot as plt
from collections import Counter
from icecream import ic

def load_data():
    """Load the extracted timeline data"""
    with open('data/extracted_timeline.json', 'r') as f:
        return json.load(f)

def parse_latlng(latlng_str):
    """Parse latitude and longitude from string format"""
    if not latlng_str:
        return None
    # Remove degree symbols and split
    clean_str = latlng_str.replace('°', '')
    lat, lng = map(float, clean_str.split(', '))
    return [lat, lng]

def analyze_locations():
    """Analyze and visualize location patterns"""
    data = load_data()
    visits = data['visits']
    activities = data['activities']
    
    # Process visit locations
    visit_locations = []
    visit_info = []
    
    for visit in visits:
        location = parse_latlng(visit.get('location'))
        if location:
            visit_locations.append(location)
            visit_info.append({
                'type': visit.get('semantic_type'),
                'start_time': visit.get('start_time'),
                'duration_str': f"{visit.get('end_time')} - {visit.get('start_time')}",
                'probability': visit.get('probability')
            })
    
    # Convert to numpy array for clustering
    X = np.array(visit_locations)
    
    # Create a map centered on the mean coordinates
    center_lat = np.mean(X[:, 0])
    center_lng = np.mean(X[:, 1])
    m = folium.Map(location=[center_lat, center_lng], zoom_start=11)
    
    # Add visit markers
    for location, info in zip(visit_locations, visit_info):
        color = 'red' if info['type'] == 'INFERRED_HOME' else 'blue'
        
        popup_content = f"""
        Type: {info['type']}<br>
        Time: {info['duration_str']}<br>
        Probability: {info['probability']:.2f}
        """
        
        folium.CircleMarker(
            location=location,
            radius=8,
            popup=popup_content,
            color=color,
            fill=True,
            fill_color=color
        ).add_to(m)
    
    # Add activity paths
    activity_coordinates = []
    
    for activity in activities:
        start = parse_latlng(activity.get('start_location'))
        end = parse_latlng(activity.get('end_location'))
        
        if start and end:
            activity_coordinates.append([start, end])
            
            # Draw path line
            folium.PolyLine(
                locations=[start, end],
                weight=2,
                color='green',
                opacity=0.8,
                popup=f"Type: {activity.get('type')}<br>Distance: {activity.get('distance_meters')}m"
            ).add_to(m)
    
    # Add heatmap layer
    heat_data = [[lat, lng] for lat, lng in visit_locations]
    plugins.HeatMap(heat_data).add_to(m)
    
    # Save the map
    m.save('output/location_analysis.html')
    ic("Map saved as 'output/location_analysis.html'")
    
    # Generate statistics
    visit_types = Counter(visit['semantic_type'] for visit in visits)
    activity_types = Counter(activity['type'] for activity in activities)
    
    stats = {
        'visits': {
            'total_locations': len(visit_locations),
            'unique_types': dict(visit_types),
            'bounds': {
                'north': float(np.max(X[:, 0])),
                'south': float(np.min(X[:, 0])),
                'east': float(np.max(X[:, 1])),
                'west': float(np.min(X[:, 1]))
            }
        },
        'activities': {
            'total_movements': len(activity_coordinates),
            'activity_types': dict(activity_types),
            'total_distance_km': sum(float(a.get('distance_meters', 0)) for a in activities) / 1000
        }
    }
    
    with open('output/location_statistics.json', 'w') as f:
        json.dump(stats, f, indent=2)
    ic("Location statistics saved to 'output/location_statistics.json'")

if __name__ == "__main__":
    analyze_locations()