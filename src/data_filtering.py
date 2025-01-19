import json
import os
from icecream import ic

# Load the original data
with open('data/detailed_places_full.json', 'r') as f:
    data = json.load(f)

def filter_place_details(place):
    google_details = place['google_details']
    
    # Keep only the absolute minimum fields needed for analysis
    filtered_details = {
        'name': google_details.get('name'),
        'geometry': {  # Keep only lat/lng from geometry
            'location': google_details.get('geometry', {}).get('location', {})
        },
        'types': google_details.get('types'),        # Essential for categorization
        'rating': google_details.get('rating'),      # Essential for quality analysis
        'price_level': google_details.get('price_level')
    }
    
    return {
        'original_data': {
            'placeId': place['original_data'].get('placeId'),
            'location': place['original_data'].get('location')
        },
        'google_details': filtered_details
    }

# Create filtered dataset
filtered_data = {
    'metadata': {
        'total_places': len(data['places']),
        'filtered_date': data['metadata'].get('filtered_date')
    },
    'places': [filter_place_details(place) for place in data['places']]
}

# Save filtered data for local use
with open('data/detailed_places.json', 'w') as f:
    json.dump(filtered_data, f, indent=2)

# Save GitHub-friendly version
with open('data/github_places.json', 'w') as f:
    json.dump(filtered_data, f)

# Print file sizes for comparison
original_size = os.path.getsize('data/detailed_places_full.json') / (1024 * 1024)  # Convert to MB
filtered_size = os.path.getsize('data/github_places.json') / (1024 * 1024)  # Convert to MB

ic(f"Original file size: {original_size:.2f} MB")
ic(f"GitHub file size: {filtered_size:.2f} MB")

# Print what we kept vs removed
if filtered_data['places']:
    example_place = filtered_data['places'][0]
    ic("Fields kept for analysis:")
    ic(list(example_place['google_details'].keys())) 