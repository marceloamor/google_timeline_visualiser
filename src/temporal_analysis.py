import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from icecream import ic

def load_data():
    """Load the extracted timeline data"""
    with open('data/extracted_timeline.json', 'r') as f:
        return json.load(f)

def analyze_temporal_patterns():
    """Analyze temporal patterns in visits and activities"""
    data = load_data()
    
    # Convert visits to DataFrame with proper timezone handling
    visits_df = pd.DataFrame(data['visits'])
    visits_df['start_time'] = pd.to_datetime(visits_df['start_time'], utc=True)
    visits_df['end_time'] = pd.to_datetime(visits_df['end_time'], utc=True)
    
    # Convert to local time using timezone offset
    visits_df['timezone_offset'] = pd.to_numeric(visits_df['timezone_offset'], errors='coerce')
    visits_df['start_time_local'] = visits_df['start_time'] + pd.to_timedelta(visits_df['timezone_offset'], unit='m')
    visits_df['end_time_local'] = visits_df['end_time'] + pd.to_timedelta(visits_df['timezone_offset'], unit='m')
    visits_df['duration_hours'] = (visits_df['end_time'] - visits_df['start_time']).dt.total_seconds() / 3600
    
    # Convert activities to DataFrame
    activities_df = pd.DataFrame(data['activities'])
    activities_df['start_time'] = pd.to_datetime(activities_df['start_time'], utc=True)
    activities_df['end_time'] = pd.to_datetime(activities_df['end_time'], utc=True)
    
    # Convert activities to local time
    activities_df['timezone_offset'] = pd.to_numeric(activities_df['timezone_offset'], errors='coerce')
    activities_df['start_time_local'] = activities_df['start_time'] + pd.to_timedelta(activities_df['timezone_offset'], unit='m')
    activities_df['end_time_local'] = activities_df['end_time'] + pd.to_timedelta(activities_df['timezone_offset'], unit='m')
    activities_df['duration_minutes'] = (activities_df['end_time'] - activities_df['start_time']).dt.total_seconds() / 60
    
    # Create visualizations
    fig = plt.figure(figsize=(20, 15))
    
    # 1. Visit durations by semantic type
    plt.subplot(3, 2, 1)
    sns.boxplot(data=visits_df, x='semantic_type', y='duration_hours')
    plt.xticks(rotation=45)
    plt.title('Visit Durations by Type')
    
    # 2. Activity durations by type
    plt.subplot(3, 2, 2)
    sns.boxplot(data=activities_df, x='type', y='duration_minutes')
    plt.xticks(rotation=45)
    plt.title('Activity Durations by Type')
    
    # 3. Visits by hour of day (local time)
    plt.subplot(3, 2, 3)
    visits_df['hour'] = visits_df['start_time_local'].dt.hour
    sns.histplot(data=visits_df, x='hour', bins=24)
    plt.title('Visits by Hour of Day (Local Time)')
    
    # 4. Activities by hour of day (local time)
    plt.subplot(3, 2, 4)
    activities_df['hour'] = activities_df['start_time_local'].dt.hour
    sns.histplot(data=activities_df, x='hour', bins=24)
    plt.title('Activities by Hour of Day (Local Time)')
    
    # 5. Visit counts by day of week
    plt.subplot(3, 2, 5)
    visits_df['day'] = visits_df['start_time_local'].dt.day_name()
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    sns.countplot(data=visits_df, x='day', order=day_order)
    plt.xticks(rotation=45)
    plt.title('Visits by Day of Week')
    
    # 6. Activity types distribution
    plt.subplot(3, 2, 6)
    sns.countplot(data=activities_df, x='type')
    plt.xticks(rotation=45)
    plt.title('Activity Types Distribution')
    
    plt.tight_layout()
    plt.savefig('output/temporal_patterns.png')
    ic("Saved temporal analysis plots to 'output/temporal_patterns.png'")
    
    # Generate statistics
    stats = {
        'visits': {
            'total_count': len(visits_df),
            'average_duration_hours': float(visits_df['duration_hours'].mean()),
            'most_common_type': visits_df['semantic_type'].mode().iloc[0],
            'date_range': {
                'start': visits_df['start_time_local'].min().isoformat(),
                'end': visits_df['end_time_local'].max().isoformat()
            }
        },
        'activities': {
            'total_count': len(activities_df),
            'average_duration_minutes': float(activities_df['duration_minutes'].mean()),
            'most_common_type': activities_df['type'].mode().iloc[0],
            'total_distance_km': float(activities_df['distance_meters'].sum() / 1000)
        }
    }
    
    with open('output/temporal_statistics.json', 'w') as f:
        json.dump(stats, f, indent=2)
    ic("Saved temporal statistics to 'output/temporal_statistics.json'")

if __name__ == "__main__":
    analyze_temporal_patterns() 