import json
import os
from icecream import ic

# Load the original data
with open('data/detailed_places_full.json', 'r') as f:
    data = json.load(f)

def filter_place_details_minimal(place):
    """Create minimal dataset for geographic analysis"""
    google_details = place['google_details']
    
    filtered_details = {
        'name': google_details.get('name'),
        'geometry': {
            'location': google_details.get('geometry', {}).get('location', {})
        },
        'types': google_details.get('types'),
        'rating': google_details.get('rating'),
        'price_level': google_details.get('price_level')
    }
    
    return {
        'original_data': {
            'placeId': place['original_data'].get('placeId'),
            'location': place['original_data'].get('location')
        },
        'google_details': filtered_details
    }

def filter_place_details_temporal(place):
    """Create dataset with temporal information"""
    google_details = place['google_details']
    
    filtered_details = {
        'name': google_details.get('name'),
        'geometry': {
            'location': google_details.get('geometry', {}).get('location', {})
        },
        'types': google_details.get('types'),
        'rating': google_details.get('rating')
    }
    
    return {
        'original_data': {
            'placeId': place['original_data'].get('placeId'),
            'location': place['original_data'].get('location'),
            'timestamp': place['original_data'].get('timestamp')  # Keep timestamp
        },
        'google_details': filtered_details
    }

# Create minimal filtered dataset
minimal_data = {
    'metadata': {
        'total_places': len(data['places']),
        'filtered_date': data['metadata'].get('filtered_date')
    },
    'places': [filter_place_details_minimal(place) for place in data['places']]
}

# Create temporal dataset
temporal_data = {
    'metadata': {
        'total_places': len(data['places']),
        'filtered_date': data['metadata'].get('filtered_date')
    },
    'places': [filter_place_details_temporal(place) for place in data['places']]
}

# Save both datasets
with open('data/github_places.json', 'w') as f:
    json.dump(minimal_data, f)

with open('data/github_places_temporal.json', 'w') as f:
    json.dump(temporal_data, f)

# Print file sizes for comparison
original_size = os.path.getsize('data/detailed_places_full.json') / (1024 * 1024)
minimal_size = os.path.getsize('data/github_places.json') / (1024 * 1024)
temporal_size = os.path.getsize('data/github_places_temporal.json') / (1024 * 1024)

ic(f"Original file size: {original_size:.2f} MB")
ic(f"Minimal file size: {minimal_size:.2f} MB")
ic(f"Temporal file size: {temporal_size:.2f} MB")

# Print what we kept vs removed
if minimal_data['places']:
    example_place = minimal_data['places'][0]
    ic("Fields kept for analysis:")
    ic(list(example_place['google_details'].keys()))

if temporal_data['places']:
    example_place = temporal_data['places'][0]
    ic("Fields kept for analysis:")
    ic(list(example_place['google_details'].keys())) 