import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import seaborn as sns
from icecream import ic

def load_data():
    with open('data/github_places_temporal.json', 'r') as f:
        return json.load(f)

def analyze_time_patterns():
    data = load_data()
    places = data['places']
    
    # Debug: Print the structure of the first place
    ic("First place structure:", places[0])
    
    # Convert timestamps to datetime objects
    visits = []
    for place in places:
        # Debug: Print available keys
        ic("Available keys in place:", place.keys())
        ic("Available keys in original_data:", place.get('original_data', {}).keys())
        
        if 'original_data' in place:
            timestamp = place['original_data'].get('timestamp')
            if timestamp:
                visits.append({
                    'time': datetime.fromtimestamp(timestamp),
                    'name': place['google_details'].get('name'),
                    'types': place['google_details'].get('types', [])
                })
    
    # Debug: Print number of visits found
    ic("Number of visits with timestamps:", len(visits))
    
    if not visits:
        ic("No timestamp data found in the filtered dataset!")
        return
        
    df = pd.DataFrame(visits)
    
    # Add time-based columns
    df['hour'] = df['time'].dt.hour
    df['day'] = df['time'].dt.day_name()
    df['month'] = df['time'].dt.month_name()
    
    # Create visualizations
    plt.figure(figsize=(15, 10))
    
    # Hourly distribution
    plt.subplot(2, 2, 1)
    sns.histplot(data=df, x='hour', bins=24)
    plt.title('Visits by Hour of Day')
    
    # Daily distribution
    plt.subplot(2, 2, 2)
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    sns.countplot(data=df, x='day', order=day_order)
    plt.xticks(rotation=45)
    plt.title('Visits by Day of Week')
    
    # Monthly distribution
    plt.subplot(2, 2, 3)
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                  'July', 'August', 'September', 'October', 'November', 'December']
    sns.countplot(data=df, x='month', order=month_order)
    plt.xticks(rotation=45)
    plt.title('Visits by Month')
    
    plt.tight_layout()
    plt.savefig('output/temporal_patterns.png')
    ic("Temporal analysis plots saved to 'output/temporal_patterns.png'")
    
    # Save statistics
    stats = {
        'busiest_hour': int(df['hour'].mode()[0]),
        'busiest_day': df['day'].mode()[0],
        'busiest_month': df['month'].mode()[0],
        'total_visits': len(df),
        'date_range': {
            'start': df['time'].min().strftime('%Y-%m-%d'),
            'end': df['time'].max().strftime('%Y-%m-%d')
        }
    }
    
    with open('output/temporal_statistics.json', 'w') as f:
        json.dump(stats, f, indent=2)
    ic("Temporal statistics saved to 'output/temporal_statistics.json'")

if __name__ == "__main__":
    analyze_time_patterns() 