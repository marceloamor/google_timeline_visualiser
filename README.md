# Google Timeline Location Analysis

A data analysis project that processes and visualizes location data from Google Timeline, providing insights into spatial patterns and place categories.

## Project Structure 
├── data/ 
│ ├── github_places.json # Filtered dataset for analysis
│ └── [other data files] # Local only, not in repository
├── output/ # Generated visualizations and analysis
│ └── .gitkeep
└── src/ # Source code
├── data_extraction.py # Google Places API data collection
├── data_filtering.py # Data processing and filtering
└── geoanalysis.py # Analysis and visualization


## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create `.env` file with your Google Places API key:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

## Current Features

- Data collection from Google Places API
- Efficient data filtering and storage
- Geographic clustering analysis
- Interactive map visualization

## Planned Features

### Phase 1: Geographic Analysis
- [ ] Heatmap visualization of visited locations
- [ ] Cluster analysis of frequently visited areas
- [ ] Time-based location patterns
- [ ] Category distribution analysis

### Phase 2: Temporal Analysis
- [ ] Daily/weekly/monthly visit patterns
- [ ] Duration of stays analysis
- [ ] Seasonal trends
- [ ] Regular vs. occasional visits

### Phase 3: Category Analysis
- [ ] Place type distribution
- [ ] Rating analysis by category
- [ ] Price level patterns
- [ ] Category clusters by geography

### Phase 4: Advanced Features
- [ ] Movement pattern analysis
- [ ] Prediction of likely destinations
- [ ] Anomaly detection
- [ ] Custom location categorization

### Phase 5: Visualization Improvements
- [ ] Interactive dashboard
- [ ] Time-lapse visualizations
- [ ] Category-based filtering
- [ ] Custom reporting

## Contributing

This is a personal project but suggestions and improvements are welcome. Please open an issue to discuss proposed changes.

## Data Privacy

This project handles personal location data. The repository only contains filtered, anonymized data for demonstration purposes. Users should be careful not to commit personal data.

## License

[Add your chosen license]

## Acknowledgments

- Google Places API for location data
- [Add other acknowledgments as needed]




# Google Timeline Analysis

A Python project to analyze and visualize Google Timeline data, providing insights into location history, movement patterns, and temporal trends.

## Setup

1. Clone this repository and place your `Timeline.json` file in the `data/` directory.

2. Initialize Poetry with your Python path:
```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```
## Project Structure

- `src/`
  - `data_extraction.py` - Extracts and structures Timeline data (visits and activities)
  - `temporal_analysis.py` - Analyzes temporal patterns in visits and movements
  - `geoanalysis.py` - Creates interactive maps and location-based visualizations

- `data/`
  - `Timeline.json` - Raw Google Timeline data
  - `extracted_timeline.json` - Processed timeline data

- `output/`
  - `temporal_patterns.png` - Visualizations of temporal patterns
  - `temporal_statistics.json` - Statistical analysis of temporal data
  - `location_analysis.html` - Interactive map visualization
  - `location_statistics.json` - Statistical analysis of locations

## Current Features

- Data Processing:
  - Extraction of both visit and activity data
  - Proper handling of timestamps and timezones
  - Structured JSON output

- Temporal Analysis:
  - Visit duration patterns
  - Activity timing analysis
  - Daily and weekly patterns
  - Time-based statistics

- Geographic Analysis:
  - Interactive map visualization
  - Visit locations with type information
  - Movement paths between locations
  - Location heatmap
  - Geographic statistics

## Future Plans

1. Enhanced Analysis:
   - Movement pattern analysis
   - Frequent route detection
   - Place categorization
   - Time spent analysis

2. Web Application:
   - Interactive dashboard
   - Data filtering options
   - Customizable visualizations
   - Timeline playback feature

3. Additional Features:
   - Export capabilities
   - Custom location tagging
   - Pattern detection
   - Statistical reporting

## Usage

1. Extract and process data:
```bash
python src/data_extraction.py
```

2. Run temporal analysis:
```bash
python src/temporal_analysis.py
```

3. Generate location visualizations:
```bash
python src/geoanalysis.py
```


## Dependencies

- Python 3.x
- Poetry for dependency management
- Required packages listed in pyproject.toml