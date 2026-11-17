
import requests
import csv
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# 5 New Cities
cities = {
    "Salem": (11.6643, 78.1460),
    "Erode": (11.3410, 77.7172),
    "Dindigul": (10.3673, 77.9803),
    "Thanjavur": (10.7870, 79.1378),
    "Nagercoil": (8.1833, 77.4119)
}

timezone = ZoneInfo("Asia/Kolkata")

# Yesterday date
yesterday = datetime.now(timezone).date() - timedelta(days=1)

date_string = yesterday.strftime("%Y-%m-%d")

all_rows = []

weather_codes = {
    0: "Clear Sky",
    1: "Mainly Clear",
    2: "Partly Cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Fog",
    51: "Drizzle",
    53: "Drizzle",
    55: "Drizzle",
    61: "Rain",
    63: "Rain",
    65: "Heavy Rain",
    71: "Snow",
    80: "Rain Showers",
    81: "Rain Showers",
    82: "Heavy Rain",
    95: "Thunderstorm"
}

for city, (lat, lon) in cities.items():

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": date_string,
        "end_date": date_string,
        "hourly": "temperature_2m,relative_humidity_2m,weather_code",
        "timezone": "Asia/Kolkata"
    }

    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()

        data = response.json()
        hourly = data["hourly"]

        print("\nProcessing:", city)

        for hour in range(6, 18):

            target_time = f"{date_string}T{hour:02d}:00"

            if target_time not in hourly["time"]:
                print("Missing:", target_time)
                continue

            index = hourly["time"].index(target_time)

            temp = hourly["temperature_2m"][index]
            humidity = hourly["relative_humidity_2m"][index]
            code = hourly["weather_code"][index]

            weather = weather_codes.get(code, "Other")

            row = {
                "Place": city,
                "Date": yesterday.strftime("%d-%m-%Y"),
                "Time": datetime.strptime(
                    target_time, "%Y-%m-%dT%H:%M"
                ).strftime("%I:%M %p"),
                "Temperature": temp,
                "Humidity": humidity,
                "Weather": weather
            }

            all_rows.append(row)

            print(
                row["Time"],
                "Humidity:", humidity,
                "Weather:", weather
            )

    except Exception as e:
        print(city, "Error:", e)


# Save CSV file
if all_rows:

    with open(
        "yesterday_weather.csv",
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        columns = [
            "Place",
            "Date",
            "Time",
            "Temperature",
            "Humidity",
            "Weather"
        ]

        writer = csv.DictWriter(
            file, fieldnames=columns
        )

        writer.writeheader()
        writer.writerows(all_rows)

    print("\nCSV FILE SAVED SUCCESSFULLY!")
    print("Total Records:", len(all_rows))
    print("File: yesterday_weather.csv")

else:
    print("No data available!")
