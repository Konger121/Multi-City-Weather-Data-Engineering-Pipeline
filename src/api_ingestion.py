import json
from pathlib import Path

import requests


BASE_URL = "https://api.open-meteo.com/v1/forecast"

CITIES = {
    "Chennai": (13.0827, 80.2707),
    "Bengaluru": (12.9716, 77.5946),
    "Hyderabad": (17.3850, 78.4867),
    "Mumbai": (19.0760, 72.8777),
    "Delhi": (28.6139, 77.2090),
    "Coimbatore": (11.0168, 76.9558),
}

OUTPUT_DIR = Path("data/raw")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def fetch_weather(city, latitude, longitude):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": [
            "temperature_2m",
            "relative_humidity_2m",
            "precipitation",
            "wind_speed_10m",
        ],
        "forecast_days": 7,
        "timezone": "auto",
    }

    response = requests.get(
        BASE_URL,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    return response.json()


def main():
    for city, (latitude, longitude) in CITIES.items():

        print(f"Fetching weather data for {city}...")

        data = fetch_weather(
            city,
            latitude,
            longitude
        )

        output_file = OUTPUT_DIR / f"{city.lower()}.json"

        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)

        print(f"Saved: {output_file}")


if __name__ == "__main__":
    main()