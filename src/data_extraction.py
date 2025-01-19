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

# Read in data 
try:
    with open('data/Timeline.json', 'r') as f:
        raw_data = json.load(f)  # Load as regular JSON first
    # Extract semanticSegments array
    segments = raw_data.get('semanticSegments', [])
    ic(f"Found {len(segments)} semantic segments")
    
    # Let's look at the first segment to understand its structure
    if segments:
        ic(segments[0])  # Show first segment structure
        
except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")
except FileNotFoundError:
    print("Timeline.json file not found")

# Extract place data including IDs and categories
place_data = []
for i, segment in enumerate(segments):
    try:
        visit = segment.get('visit', {})
        top_candidate = visit.get('topCandidate', {})
        
        place_info = {
            'placeId': top_candidate.get('placeId'),
            'location': top_candidate.get('placeLocation', {}),
            'name': top_candidate.get('name', 'Unknown'),
            'categories': top_candidate.get('categories', [])
        }
        
        if place_info['placeId']:  # Only append if we have a valid placeId
            place_data.append(place_info)
            
    except AttributeError as e:
        print(f"Error processing segment {i}: {e}")

ic(f"Found {len(place_data)} places with IDs")
if place_data:
    ic(place_data[0])  # Show example of what we extracted

# Initialize Google Maps client
gmaps = Client(key=GOOGLE_API_KEY)

# Constants
COST_PER_REQUEST = 0.017   # Current cost in USD per place details request
MAX_TOTAL_COST = 190       # Maximum cost in USD we're willing to spend
MAX_REQUESTS = int(MAX_TOTAL_COST / COST_PER_REQUEST)  # About 11,176 requests
REQUESTS_PER_SECOND = 50   # Aggressive but safe rate limiting

# Get all available fields from Places API
PLACE_FIELDS = [
    'address_component', 'adr_address', 'business_status', 'formatted_address',
    'geometry', 'icon', 'name', 'photo', 'place_id', 'plus_code', 'type',
    'url', 'utc_offset', 'vicinity', 'formatted_phone_number',
    'international_phone_number', 'opening_hours', 'website', 
    'price_level', 'rating', 'review', 'user_ratings_total'
]

def get_place_details(place_id, request_count):
    if request_count >= MAX_REQUESTS:
        print(f"Approaching cost limit (${MAX_TOTAL_COST})! Stopping requests.")
        return None
    
    try:
        time.sleep(1.0/REQUESTS_PER_SECOND)  # Minimal rate limiting
        result = gmaps.place(place_id, fields=PLACE_FIELDS)
        current_cost = (request_count + 1) * COST_PER_REQUEST
        if request_count % 100 == 0:  # Print status every 100 requests
            ic(f"Requests made: {request_count + 1}, Current cost: ${current_cost:.2f}")
        return result['result']
    except Exception as e:
        print(f"Error fetching place details for {place_id}: {e}")
        return None

# Process all places and save detailed data
detailed_places = []
request_count = 0

print(f"Starting to process {len(place_data)} places...")
print(f"Maximum requests allowed: {MAX_REQUESTS} (to stay under ${MAX_TOTAL_COST})")

for i, place in enumerate(place_data):
    if request_count >= MAX_REQUESTS:
        print("Reached maximum request limit!")
        break
        
    details = get_place_details(place['placeId'], request_count)
    if details:
        request_count += 1
        detailed_places.append({
            'original_data': place,
            'google_details': details,
            'fetch_time': datetime.now().isoformat()
        })
        
        # Save progress every 100 places
        if len(detailed_places) % 100 == 0:
            with open('data/detailed_places_full.json', 'w') as f:
                json.dump({
                    'metadata': {
                        'total_places_processed': len(detailed_places),
                        'total_cost': request_count * COST_PER_REQUEST,
                        'last_update': datetime.now().isoformat(),
                        'total_places_available': len(place_data)
                    },
                    'places': detailed_places
                }, f, indent=2)
            ic(f"Progress saved: {len(detailed_places)} places processed")

# Final save
with open('data/detailed_places_full.json', 'w') as f:
    json.dump({
        'metadata': {
            'total_places_processed': len(detailed_places),
            'total_cost': request_count * COST_PER_REQUEST,
            'last_update': datetime.now().isoformat(),
            'total_places_available': len(place_data),
            'processing_complete': request_count < len(place_data)
        },
        'places': detailed_places
    }, f, indent=2)

print(f"\nProcessing complete!")
print(f"Total places processed: {len(detailed_places)}")
print(f"Total cost: ${(request_count * COST_PER_REQUEST):.2f}")
print(f"Data saved to 'data/detailed_places_full.json'")

# Create a summary of the data we've collected
if detailed_places:
    place_types = collections.Counter()
    ratings = []
    price_levels = collections.Counter()
    
    for place in detailed_places:
        details = place['google_details']
        place_types.update(details.get('types', []))
        if 'rating' in details:
            ratings.append(details['rating'])
        if 'price_level' in details:
            price_levels.update([details['price_level']])

    # Save summary statistics
    with open('data/place_statistics.json', 'w') as f:
        json.dump({
            'common_types': dict(place_types.most_common(20)),
            'rating_stats': {
                'average': sum(ratings) / len(ratings) if ratings else 0,
                'count': len(ratings),
                'distribution': {str(i): ratings.count(i) for i in range(1, 6)}
            },
            'price_level_distribution': dict(price_levels)
        }, f, indent=2)

    ic("Statistics saved to 'data/place_statistics.json'")