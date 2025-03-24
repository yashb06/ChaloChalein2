import requests

API_KEY = "6646d76918a04273941173000252003"  # New WeatherAPI key

def get_weather_forecast(city):
    """
    Get weather forecast for a given location using WeatherAPI.
    """
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&aqi=no"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "location": data["location"]["name"],
            "temperature": data["current"]["temp_c"],
            "description": data["current"]["condition"]["text"]
        }
    else:
        return {"error": "Unable to fetch weather data"}

def get_location_coordinates(location):
    """
    Get coordinates for a given location. Placeholder implementation.
    """
    return {"latitude": 0.0, "longitude": 0.0}
