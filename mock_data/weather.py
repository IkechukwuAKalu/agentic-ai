from typing import Any, Dict, List

def call_weather_api(date: str) -> Dict[str, Any]:
    data = get_weather_data()

    data = {item["date"]: item for item in data}

    return data[date]


def get_weather_data() -> List[Dict[str, Any]]:
    return [
        {
            "date": "2024-01-10",
            "temperature": {"fahrenheit": 23.4, "celsius": -4.8},
            "conditions": {
                "main": "Clear",
                "precipitation": "None",
                "precipitation_amount": 0,
                "special_event": None,
            },
        },
        {
            "date": "2024-01-11",
            "temperature": {"fahrenheit": 39.3, "celsius": 4.1},
            "conditions": {
                "main": "Clear",
                "precipitation": "None",
                "precipitation_amount": 0,
                "special_event": None,
            },
        },
        {
            "date": "2024-01-12",
            "temperature": {"fahrenheit": 41.1, "celsius": 5.1},
            "conditions": {
                "main": "Heavy Rain",
                "precipitation": "Heavy Rain",
                "precipitation_amount": 2.7,
                "special_event": "Flood Warning",
            },
        },
        {
            "date": "2024-01-13",
            "temperature": {"fahrenheit": 27.2, "celsius": -2.6},
            "conditions": {
                "main": "Clear",
                "precipitation": "None",
                "precipitation_amount": 0,
                "special_event": None,
            },
        },
        {
            "date": "2024-01-14",
            "temperature": {"fahrenheit": 22.9, "celsius": -5.1},
            "conditions": {
                "main": "Clear",
                "precipitation": "None",
                "precipitation_amount": 0,
                "special_event": None,
            },
        },
        {
            "date": "2024-01-15",
            "temperature": {"fahrenheit": 33.2, "celsius": 0.7},
            "conditions": {
                "main": "Clear",
                "precipitation": "None",
                "precipitation_amount": 0,
                "special_event": "High Winds",
            },
        },
        {
            "date": "2024-01-16",
            "temperature": {"fahrenheit": 23.3, "celsius": -4.8},
            "conditions": {
                "main": "Clear",
                "precipitation": "None",
                "precipitation_amount": 0,
                "special_event": None,
            },
        },
    ]