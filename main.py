import os
import requests
from datetime import datetime


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
        2: "Parțial înnorat",
        3: "Înnorat",
        45: "Ceață",
        48: "Ceață depunătoare",
        51: "Burniță ușoară",
        53: "Burniță moderată",
        55: "Burniță puternică",
        61: "Ploaie slabă",
        63: "Ploaie moderată",
        65: "Ploaie puternică",
        71: "Ninsoare slabă",
        73: "Ninsoare moderată",
        75: "Ninsoare puternică",
        80: "Averse ușoare",
        81: "Averse moderate",
        82: "Averse puternice",
    }
    return mapping.get(code, "Condiții meteo necunoscute")


def main():
    # Coordonate default: București
    latitude = float(os.getenv("LATITUDE", "44.4268"))
    longitude = float(os.getenv("LONGITUDE", "26.1025"))
    city_name = os.getenv("CITY_NAME", "București")

    try:
        weather = get_weather(latitude, longitude)
    except Exception as e:
        print(f"[ERROR] Failed to fetch weather data: {e}")
        return

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    description = describe_weather_code(weather.get("weathercode"))

    print("===== Daily Weather Report =====")
    print(f"Generat la: {now}")
    print(f"Locație: {city_name} (lat={latitude}, lon={longitude})")
    print("")
    print(f"Timp API: {weather.get('time')}")
    print(f"Temperatură: {weather.get('temperature')} °C")
    print(f"Viteza vântului: {weather.get('windspeed')} km/h")
    print(f"Direcția vântului: {weather.get('winddirection')}°")
    print(f"Condiții: {description}")
    print("================================")


if __name__ == "__main__":
    main()
