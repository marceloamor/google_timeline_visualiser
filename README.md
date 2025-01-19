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