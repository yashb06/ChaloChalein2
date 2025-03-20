import requests
import streamlit as st
from datetime import datetime

def get_weather_forecast(lat, lng, date):
    """
    Get weather forecast for the specified location and date
    """
    api_key = st.secrets["WHEATHER_API"]
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lng}&appid={api_key}&units=metric"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Find forecast closest to the target date
        target_date = datetime.combine(date, datetime.min.time())
        
        for forecast in data['list']:
            forecast_date = datetime.fromtimestamp(forecast['dt'])
            if forecast_date.date() == target_date.date():
                return {
                    'temperature': forecast['main']['temp'],
                    'description': forecast['weather'][0]['description'],
                    'humidity': forecast['main']['humidity']
                }
    return None

def get_location_coordinates(location_name):
    """
    Get coordinates for a location using Google Maps Geocoding API
    """
    api_key = st.secrets["GOOGLE_MAPS_API_KEY"]
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location_name}&key={api_key}"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            location = data['results'][0]['geometry']['location']
            return {
                'lat': location['lat'],
                'lng': location['lng']
            }
    return None
