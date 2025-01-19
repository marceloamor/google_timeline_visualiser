import json
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import folium
from folium.plugins import MarkerCluster
import pandas as pd
from icecream import ic
import matplotlib.pyplot as plt
from collections import Counter
import os

# Load the original data
with open('detailed_places_full.json', 'r') as f:
    data = json.load(f)

def filter_place_details(place):
    google_details = place['google_details']
    
    # Keep these essential fields for analysis
    filtered_details = {
        'name': google_details.get('name'),
        'place_id': google_details.get('place_id'),
        'geometry': google_details.get('geometry'),  # Essential for spatial analysis
        'types': google_details.get('types'),        # Essential for categorization
        'rating': google_details.get('rating'),      # Essential for quality analysis
        'formatted_address': google_details.get('formatted_address'),
        'price_level': google_details.get('price_level'),
        'user_ratings_total': google_details.get('user_ratings_total'),
        'business_status': google_details.get('business_status'),
        'opening_hours': google_details.get('opening_hours', {}).get('periods'),  # Keep just the periods
        'utc_offset': google_details.get('utc_offset')
    }
    
    # Keep only 2 most recent reviews with limited fields
    if 'reviews' in google_details:
        filtered_details['reviews'] = [{
            'rating': review.get('rating'),
            'time': review.get('time'),
            'relative_time_description': review.get('relative_time_description')
        } for review in google_details['reviews'][:2]]
    
    # Remove photos entirely as they're mostly URLs and not essential for analysis
    
    return {
        'original_data': {
            'placeId': place['original_data'].get('placeId'),
            'location': place['original_data'].get('location'),
            'name': place['original_data'].get('name'),
            'categories': place['original_data'].get('categories')
        },
        'google_details': filtered_details,
        'fetch_time': place['fetch_time']
    }

# Create filtered dataset
filtered_data = {
    'metadata': data['metadata'],
    'places': [filter_place_details(place) for place in data['places']]
}

# Save filtered data
with open('detailed_places.json', 'w') as f:
    json.dump(filtered_data, f, indent=2)

# Print file sizes for comparison
original_size = os.path.getsize('detailed_places_full.json') / (1024 * 1024)  # Convert to MB
filtered_size = os.path.getsize('detailed_places.json') / (1024 * 1024)  # Convert to MB

ic(f"Original file size: {original_size:.2f} MB")
ic(f"Filtered file size: {filtered_size:.2f} MB")

# Print what we kept vs removed
if filtered_data['places']:
    example_place = filtered_data['places'][0]
    ic("Fields kept for analysis:")
    ic(list(example_place['google_details'].keys()))

# Extract coordinates and metadata
locations = []
place_info = []

for place in data['places']:
    try:
        details = place['google_details']
        geometry = details.get('geometry', {})
        location = geometry.get('location', {})
        
        if location and 'lat' in location and 'lng' in location:
            locations.append([location['lat'], location['lng']])
            place_info.append({
                'name': details.get('name', 'Unknown'),
                'types': details.get('types', []),
                'rating': details.get('rating'),
                'address': details.get('formatted_address')
            })
    except KeyError as e:
        print(f"Error processing place: {e}")

# Convert to numpy array for clustering
X = np.array(locations)

# Perform DBSCAN clustering
# eps is in degrees (roughly 1km at the equator)
eps_km = 1.0  # 1km cluster radius
eps = eps_km / 111.32  # Convert km to degrees (approximate)
db = DBSCAN(eps=eps, min_samples=5).fit(X)

# Get cluster labels
labels = db.labels_

# Count number of clusters (excluding noise points labeled as -1)
n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
ic(f"Number of clusters: {n_clusters}")

# Create a map centered on the mean coordinates
center_lat = np.mean(X[:, 0])
center_lng = np.mean(X[:, 1])
m = folium.Map(location=[center_lat, center_lng], zoom_start=10)

# Create a color map for clusters
colors = plt.cm.rainbow(np.linspace(0, 1, n_clusters))
color_map = {i: '#%02x%02x%02x' % tuple(int(255*j) for j in c[:3]) 
            for i, c in enumerate(colors)}
color_map[-1] = '#808080'  # Gray for noise points

# Add points to map with cluster colors
for idx, (point, label, info) in enumerate(zip(X, labels, place_info)):
    color = color_map[label]
    
    # Create popup content
    popup_content = f"""
    <b>{info['name']}</b><br>
    Types: {', '.join(info['types'][:3])}<br>
    Rating: {info['rating']}<br>
    Address: {info['address']}<br>
    Cluster: {'Noise' if label == -1 else label}
    """
    
    folium.CircleMarker(
        location=point,
        radius=8,
        popup=popup_content,
        color=color,
        fill=True,
        fill_color=color
    ).add_to(m)

# Save the map
m.save('location_clusters.html')
ic("Map saved as 'location_clusters.html'")

# Analyze clusters
cluster_stats = {}
for label in set(labels):
    if label != -1:  # Exclude noise points
        cluster_points = X[labels == label]
        cluster_info = [info for i, info in enumerate(place_info) if labels[i] == label]
        
        # Get most common place types in cluster
        all_types = [type for place in cluster_info for type in place['types']]
        common_types = Counter(all_types).most_common(3)
        
        cluster_stats[label] = {
            'size': len(cluster_points),
            'center': cluster_points.mean(axis=0).tolist(),
            'common_types': common_types,
            'avg_rating': np.mean([p['rating'] for p in cluster_info if p['rating'] is not None])
        }

# Fix for JSON serialization of numpy types
def convert_to_serializable(obj):
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    return obj

# Save cluster statistics with fixed serialization
with open('cluster_statistics.json', 'w') as f:
    serializable_stats = {
        'total_clusters': int(n_clusters),  # Convert numpy.int64 to regular int
        'noise_points': int(list(labels).count(-1)),
        'cluster_stats': {
            str(k): {  # Convert cluster label to string
                'size': int(v['size']),
                'center': [float(c) for c in v['center']],
                'common_types': v['common_types'],
                'avg_rating': float(v['avg_rating']) if not np.isnan(v['avg_rating']) else None
            }
            for k, v in cluster_stats.items()
        }
    }
    json.dump(serializable_stats, f, indent=2)

ic("Cluster statistics saved to 'cluster_statistics.json'")

