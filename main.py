import os
import requests
from datetime import datetime
from pathlib import Path
import csv


def get_weather(latitude: float, longitude: float):
    """Fetch current weather data from Open-Meteo API."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": True,
        "timezone": "auto",
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    current = data.get("current_weather", {})
    return {
        "time": current.get("time"),
        "temperature": current.get("temperature"),
        "windspeed": current.get("windspeed"),
        "winddirection": current.get("winddirection"),
        "weathercode": current.get("weathercode"),
    }


def describe_weather_code(code: int) -> str:
    """Very simple description for Open-Meteo weather codes."""
    mapping = {
        0: "Cer senin",
        1: "Mai mult senin",
        2: "Partial înnorat",
        3: "Innorat",
        45: "Ceata",
        48: "Ceata depunatoare",
        51: "Burnita usoara",
        53: "Burnita moderata",
        55: "Burnita puternica",
        61: "Ploaie slaba",
        63: "Ploaie moderata",
        65: "Ploaie puternica",
        71: "Ninsoare slaba",
        73: "Ninsoare moderata",
        75: "Ninsoare puternica",
        80: "Averse usoare",
        81: "Averse moderate",
        82: "Averse puternice",
    }
    return mapping.get(code, "Conditii meteo necunoscute")

def append_to_log(
    city_name: str,
    latitude: float,
    longitude: float,
    weather: dict,
    log_path: Path | None = None,
):
    """Append current weather data to a CSV log file."""
    if log_path is None:
        log_path = Path("weather_log.csv")

    file_exists = log_path.exists()

    now_local = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    api_time = weather.get("time")
    temperature = weather.get("temperature")
    windspeed = weather.get("windspeed")
    winddirection = weather.get("winddirection")
    code = weather.get("weathercode")
    description = describe_weather_code(code)

    with log_path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # Scriem header dacă fișierul e nou
        if not file_exists:
            writer.writerow([
                "logged_at",
                "api_time",
                "city",
                "latitude",
                "longitude",
                "temperature_c",
                "windspeed_kmh",
                "winddirection_deg",
                "weather_code",
                "description_ro",
            ])
        writer.writerow([
            now_local,
            api_time,
            city_name,
            latitude,
            longitude,
            temperature,
            windspeed,
            winddirection,
            code,
            description,
        ])



def main():
    # Coordonate default: București
    latitude = float(os.getenv("LATITUDE", "44.4268"))
    longitude = float(os.getenv("LONGITUDE", "26.1025"))
    city_name = os.getenv("CITY_NAME", "Bucuresti")

    try:
        weather = get_weather(latitude, longitude)
    except Exception as e:
        print(f"[ERROR] Failed to fetch weather data: {e}")
        return

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    description = describe_weather_code(weather.get("weathercode"))

    print("===== Daily Weather Report =====")
    print(f"Generat la: {now}")
    print(f"Locatie: {city_name} (lat={latitude}, lon={longitude})")
    print("")
    print(f"Timp API: {weather.get('time')}")
    print(f"Temperatura: {weather.get('temperature')} °C")
    print(f"Viteza vantului: {weather.get('windspeed')} km/h")
    print(f"Directia vantului: {weather.get('winddirection')}°")
    print(f"Conditii: {description}")
    print("================================")

     # Salvarea pentru jurnal
    append_to_log(city_name, latitude, longitude, weather)



if __name__ == "__main__":
    main()