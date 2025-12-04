from pathlib import Path
import csv
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from main import describe_weather_code, append_to_log


def test_describe_weather_code_known_values():
    assert describe_weather_code(0) == "Cer senin"
    assert describe_weather_code(3) == "Înnorat"
    assert describe_weather_code(61) == "Ploaie slabă"


def test_describe_weather_code_unknown_value():
    # un cod care nu e în mapping
    assert describe_weather_code(999) == "Condiții meteo necunoscute"


def test_append_to_log_creates_file_and_header(tmp_path):
    # folosim un fișier temporar ca să nu stricăm weather_log.csv real
    log_path = tmp_path / "weather_log.csv"

    fake_weather = {
        "time": "2025-12-04T10:00",
        "temperature": 10.5,
        "windspeed": 5.0,
        "winddirection": 180,
        "weathercode": 0,
    }

    append_to_log("Test City", 1.23, 4.56, fake_weather, log_path=log_path)

    assert log_path.exists()

    # citim conținutul CSV-ului și verificăm header + un rând
    with log_path.open("r", encoding="utf-8") as f:
        reader = list(csv.reader(f))

    # primul rând = header
    header = reader[0]
    assert header == [
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
    ]

    # al doilea rând = datele noastre
    row = reader[1]
    assert row[2] == "Test City"
    assert float(row[3]) == 1.23
    assert float(row[4]) == 4.56
    assert float(row[5]) == 10.5
