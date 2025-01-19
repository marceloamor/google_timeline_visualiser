import json
import numpy as np
from sklearn.cluster import DBSCAN
import folium
import matplotlib.pyplot as plt
from collections import Counter
from icecream import ic

# Load the filtered data
with open('data/github_places.json', 'r') as f:
    data = json.load(f)
    places = data['places']

# Extract coordinates and metadata
locations = []
place_info = []

# Print first place data for debugging
ic("First place in data:", places[0])

for place in places:
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
        ic(f"Error processing place: {e}")

# Convert to numpy array for clustering
X = np.array(locations)

# Perform DBSCAN clustering
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
m.save('output/location_clusters.html')
ic("Map saved as 'output/location_clusters.html'")

# Analyze clusters
cluster_stats = {}
for label in set(labels):
    if label != -1:  # Exclude noise points
        cluster_points = X[labels == label]
        cluster_info = [info for i, info in enumerate(place_info) if labels[i] == label]
        
        # Get most common place types in cluster
        all_types = [type for place in cluster_info for type in place['types']]
        common_types = Counter(all_types).most_common(3)
        
        # Handle empty ratings more gracefully
        valid_ratings = [p['rating'] for p in cluster_info if p['rating'] is not None]
        avg_rating = float(np.mean(valid_ratings)) if valid_ratings else None
        
        cluster_stats[str(label)] = {  # Convert label to string for JSON
            'size': int(len(cluster_points)),  # Convert numpy.int64 to regular int
            'center': [float(x) for x in cluster_points.mean(axis=0)],  # Convert to regular float
            'common_types': common_types,
            'avg_rating': avg_rating
        }

# Save cluster statistics
with open('output/cluster_statistics.json', 'w') as f:
    json.dump({
        'total_clusters': int(n_clusters),  # Convert numpy.int64 to regular int
        'noise_points': int(list(labels).count(-1)),
        'cluster_stats': cluster_stats
    }, f, indent=2)

ic("Cluster statistics saved to 'output/cluster_statistics.json'")