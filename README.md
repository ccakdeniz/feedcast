# FeedCast
A smart nutrient application advisor.

### How it works:
- **Geo-Location:** Uses browser API to find your lawn's coordinates.
- **Weather Integration:** Pulls 10-day data from Open-Meteo.
- **The "Sunday Logic":** Analyzes temperature and precipitation windows.
- **Look-Ahead:** Automatically downgrades "Green" days if a washout is predicted for the following day.

### Tech Stack:
- Python / Django
- JavaScript (Leaflet.js for Mapping)
- CSS3 (Flexbox/Grid)
