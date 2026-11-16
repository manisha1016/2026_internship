# Weather Data Collector

This project fetches yesterday's weather data for five cities in Tamil Nadu using the Open-Meteo API and saves the result as a CSV file.

## What it does

The script in [weather.py](weather.py):

- Fetches daily weather information for:
  - Salem
  - Erode
  - Dindigul
  - Thanjavur
  - Nagercoil
- Uses the previous date from the local timezone: Asia/Kolkata
- Requests hourly weather details for each city
- Collects data between 06:00 and 17:00 for the selected day
- Saves records into a CSV file named `yesterday_weather.csv`

## Weather data included

Each row contains:

- Place
- Date
- Time
- Temperature
- Humidity
- Weather

## Requirements

Before running the script, install the required package:

```bash
pip install requests
```

## Run the script

```bash
python weather.py
```

## Output

After execution, the script creates:

```text
yesterday_weather.csv
```

This file contains weather observations for all cities in the selected time range.

## Notes

- The script uses the Open-Meteo forecast API.
- It is configured for the Asia/Kolkata timezone.
- If any city data is missing for a selected hour, the script skips that time and continues processing the rest.
