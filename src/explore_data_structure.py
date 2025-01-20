import json
from icecream import ic
from collections import defaultdict

def explore_structure(data, max_samples=5):
    """Explore the structure of Timeline.json data"""
    
    segments = data.get('semanticSegments', [])
    ic("Total segments:", len(segments))
    
    # Separate activities and visits
    activity_segments = [s for s in segments if 'activity' in s]
    visit_segments = [s for s in segments if 'visit' in s]
    
    ic("Number of activity segments:", len(activity_segments))
    ic("Number of visit segments:", len(visit_segments))
    
    # Analyze activity segments
    ic("\nEXAMINING ACTIVITY SEGMENTS:")
    for i, segment in enumerate(activity_segments[:max_samples]):
        ic(f"\nActivity {i}:")
        ic("Time range:", {
            'start': segment.get('startTime'),
            'end': segment.get('endTime'),
            'timezone_offset': segment.get('startTimeTimezoneUtcOffsetMinutes')
        })
        
        activity = segment['activity']
        ic("Activity data:", {
            'type': activity.get('topCandidate', {}).get('type'),
            'probability': activity.get('topCandidate', {}).get('probability'),
            'distance_meters': activity.get('distanceMeters'),
            'start_location': activity.get('start', {}).get('latLng'),
            'end_location': activity.get('end', {}).get('latLng')
        })
    
    # Analyze visit segments
    ic("\nEXAMINING VISIT SEGMENTS:")
    for i, segment in enumerate(visit_segments[:max_samples]):
        ic(f"\nVisit {i}:")
        ic("Time range:", {
            'start': segment.get('startTime'),
            'end': segment.get('endTime'),
            'timezone_offset': segment.get('startTimeTimezoneUtcOffsetMinutes')
        })
        
        visit = segment['visit']
        top_candidate = visit.get('topCandidate', {})
        ic("Visit data:", {
            'hierarchy_level': visit.get('hierarchyLevel'),
            'probability': visit.get('probability'),
            'place_id': top_candidate.get('placeId'),
            'semantic_type': top_candidate.get('semanticType'),
            'location': top_candidate.get('placeLocation', {}).get('latLng')
        })
    
    # Verify structure consistency
    ic("\nVERIFYING STRUCTURE CONSISTENCY:")
    activity_structures = defaultdict(int)
    visit_structures = defaultdict(int)
    
    for segment in activity_segments:
        key = tuple(sorted(segment['activity'].keys()))
        activity_structures[key] += 1
    
    for segment in visit_segments:
        key = tuple(sorted(segment['visit'].keys()))
        visit_structures[key] += 1
    
    ic("Unique activity structures found:", len(activity_structures))
    ic("Activity structure frequencies:", dict(activity_structures))
    
    ic("Unique visit structures found:", len(visit_structures))
    ic("Visit structure frequencies:", dict(visit_structures))

if __name__ == "__main__":
    with open('data/Timeline.json', 'r') as f:
        data = json.load(f)
    
    explore_structure(data) 