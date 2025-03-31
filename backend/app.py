from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import requests
import firebase_admin
from firebase_admin import credentials, auth
import os
from datetime import datetime, timedelta
from geopy.geocoders import Nominatim
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Validate GROQ API key on startup
def validate_groq_api_key():
    """Validate that the GROQ API key is properly configured and working"""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key or api_key == "your_groq_api_key":
        print("WARNING: GROQ_API_KEY is not properly configured. Using fallback data.")
        return False
    
    try:
        # Test the API key with a simple request
        from langchain_groq import ChatGroq
        
        llm = ChatGroq(
            temperature=0.2,
            api_key=api_key,
            model_name="llama-3.3-70b-versatile"
        )
        
        # Simple test prompt
        response = llm.invoke("Hello, are you working?")
        if response and hasattr(response, 'content'):
            print("GROQ API connection successful!")
            return True
        else:
            print("WARNING: GROQ API connection failed. Using fallback data.")
            return False
    except Exception as e:
        print(f"ERROR connecting to GROQ API: {str(e)}. Using fallback data.")
        return False

# Check API connection on startup
GROQ_API_AVAILABLE = validate_groq_api_key()

# Initialize Firebase
try:
    cred = credentials.Certificate("firebase-credentials.json")
    firebase_admin.initialize_app(cred)
except (ValueError, FileNotFoundError):
    # App already initialized or credentials file not found
    pass

app = FastAPI(title="ChaloChalein API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Weather API key
API_KEY = "6646d76918a04273941173000252003"

# Models
class UserLogin(BaseModel):
    email: str
    password: str

class UserSignup(BaseModel):
    email: str
    password: str

class ChatRequest(BaseModel):
    city: str
    startDate: str
    endDate: str
    travelingVia: str
    travelingWith: str
    interests: List[str]
    message: Optional[str] = None

class WeatherRequest(BaseModel):
    city: str

class ItineraryRequest(BaseModel):
    city: str
    startDate: str
    endDate: str
    interests: List[str]
    travelingVia: str

class LocationRequest(BaseModel):
    city: str
    query: Optional[str] = None

# Helper functions
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
    Get coordinates for a given location using Nominatim.
    """
    try:
        geolocator = Nominatim(user_agent="travel_chatbot")
        location_data = geolocator.geocode(location)
        if location_data:
            return {
                "latitude": location_data.latitude,
                "longitude": location_data.longitude
            }
        return {"latitude": 0.0, "longitude": 0.0}
    except Exception as e:
        print(f"Error getting coordinates: {str(e)}")
        return {"latitude": 0.0, "longitude": 0.0}

# Routes
@app.post("/api/auth/login")
async def login(user_data: UserLogin):
    try:
        # In a real app, you would verify the password here
        user = auth.get_user_by_email(user_data.email)
        return {"success": True, "email": user_data.email}
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/api/auth/signup")
async def signup(user_data: UserSignup):
    try:
        user = auth.create_user(
            email=user_data.email,
            password=user_data.password
        )
        return {"success": True, "email": user_data.email}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating account: {str(e)}")

@app.post("/api/weather")
async def weather(request: WeatherRequest):
    try:
        weather_data = get_weather_forecast(request.city)
        return weather_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching weather: {str(e)}")

@app.post("/api/itinerary")
async def generate_itinerary(request: ItineraryRequest):
    try:
        # Check if GROQ_API_KEY is available and validated
        if not GROQ_API_AVAILABLE:
            print("Warning: GROQ_API not available. Using fallback itinerary.")
            return get_fallback_itinerary(request)
            
        # Parse dates and calculate duration
        start_date = datetime.strptime(request.startDate, "%Y-%m-%d")
        end_date = datetime.strptime(request.endDate, "%Y-%m-%d")
        duration = (end_date - start_date).days + 1
        
        # Initialize the LLM
        groq_api_key = os.environ.get("GROQ_API_KEY")
        llm = ChatGroq(
            temperature=0.2,
            api_key=groq_api_key,
            model_name="llama-3.3-70b-versatile"
        )
        
        # Create a more detailed prompt
        prompt = ChatPromptTemplate.from_template(
            """You are a travel planning assistant. Create a detailed itinerary for a trip to {city}.
            The trip starts on {start_date} and ends on {end_date}, lasting {duration} days.
            The traveler is interested in {interests} and will be traveling via {travel_mode}.
            
            For each day, provide:
            1. A morning activity (around 9-10 AM)
            2. A lunch recommendation (around 12-1 PM)
            3. An afternoon activity (around 2-4 PM)
            4. An evening activity or dinner recommendation (around 6-8 PM)
            
            Consider the following:
            - Include specific location names that actually exist in {city}
            - Suggest local cuisine and authentic experiences
            - Balance tourist attractions with off-the-beaten-path experiences
            - Consider the weather and seasonal activities appropriate for the time of year
            - Group activities by proximity to minimize travel time
            
            Format the response as a JSON array with each day as an object containing:
            - day: the day number
            - date: the date in YYYY-MM-DD format
            - activities: an array of activities with time, description, and location
            
            Example format:
            [
              {{
                "day": 1,
                "date": "2023-06-01",
                "activities": [
                  {{
                    "time": "09:00",
                    "description": "Visit the Eiffel Tower",
                    "location": "Champ de Mars, 5 Avenue Anatole France"
                  }},
                  {{
                    "time": "12:30",
                    "description": "Lunch at Café de Flore",
                    "location": "172 Boulevard Saint-Germain"
                  }}
                ]
              }}
            ]
            
            Return ONLY the JSON array with no additional text.
            """
        )
        
        # Format the interests as a comma-separated string
        interests_str = ", ".join(request.interests)
        
        # Generate the itinerary
        formatted_prompt = prompt.format(
            city=request.city,
            start_date=request.startDate,
            end_date=request.endDate,
            duration=duration,
            interests=interests_str,
            travel_mode=request.travelingVia
        )
        
        print(f"Generating itinerary for {request.city} from {request.startDate} to {request.endDate}")
        response = llm.invoke(formatted_prompt)
        
        # Extract JSON from the response
        json_str = extract_json_from_response(response.content)
        
        # Parse the JSON
        import json
        try:
            itinerary_data = json.loads(json_str)
            print(f"Successfully generated itinerary with {len(itinerary_data)} days")
            return {"itinerary": itinerary_data}
        except json.JSONDecodeError:
            print(f"Failed to parse JSON from response: {json_str}")
            return get_fallback_itinerary(request)
            
    except Exception as e:
        print(f"Error generating itinerary: {str(e)}")
        return get_fallback_itinerary(request)

def extract_json_from_response(content):
    """Extract JSON from the LLM response"""
    # Check if the entire content is JSON
    import json
    try:
        json.loads(content)
        return content
    except json.JSONDecodeError:
        pass
        
    # Try to extract JSON from markdown code blocks
    if "```json" in content:
        json_start = content.find("```json") + 7
        json_end = content.find("```", json_start)
        if json_end > json_start:
            json_str = content[json_start:json_end].strip()
            return json_str
            
    elif "```" in content:
        json_start = content.find("```") + 3
        json_end = content.find("```", json_start)
        if json_end > json_start:
            json_str = content[json_start:json_end].strip()
            return json_str
                
    # Look for content that appears to be JSON (surrounded by curly braces)
    import re
    json_pattern = r'(\[[\s\S]*\])'
    match = re.search(json_pattern, content)
    if match:
        return match.group(1)
        
    # If all else fails, return the original content
    return content

def get_fallback_itinerary(request):
    """Provide a fallback itinerary when API calls fail"""
    # Parse dates
    start_date = datetime.strptime(request.startDate, "%Y-%m-%d")
    end_date = datetime.strptime(request.endDate, "%Y-%m-%d")
    duration = (end_date - start_date).days + 1
    
    # Common activities by city
    city_activities = {
        "paris": [
            {"time": "09:00", "description": "Visit the Eiffel Tower", "location": "Champ de Mars, 5 Avenue Anatole France"},
            {"time": "12:30", "description": "Lunch at Café de Flore", "location": "172 Boulevard Saint-Germain"},
            {"time": "14:00", "description": "Explore the Louvre Museum", "location": "Rue de Rivoli, 75001"},
            {"time": "18:00", "description": "Dinner at Le Comptoir du Relais", "location": "9 Carrefour de l'Odéon"},
            {"time": "09:30", "description": "Visit Notre-Dame Cathedral", "location": "6 Parvis Notre-Dame - Pl. Jean-Paul II"},
            {"time": "12:00", "description": "Lunch at L'As du Fallafel", "location": "34 Rue des Rosiers"},
            {"time": "14:30", "description": "Stroll through Montmartre", "location": "Place du Tertre"},
            {"time": "19:00", "description": "Dinner cruise on the Seine", "location": "Port de la Bourdonnais"},
            {"time": "10:00", "description": "Visit Musée d'Orsay", "location": "1 Rue de la Légion d'Honneur"},
            {"time": "13:00", "description": "Lunch at Angelina", "location": "226 Rue de Rivoli"},
            {"time": "15:00", "description": "Shop on Champs-Élysées", "location": "Avenue des Champs-Élysées"},
            {"time": "20:00", "description": "Dinner at Le Jules Verne", "location": "Eiffel Tower, 2nd floor"}
        ],
        "london": [
            {"time": "09:00", "description": "Visit the Tower of London", "location": "Tower Hill"},
            {"time": "12:30", "description": "Lunch at Borough Market", "location": "8 Southwark Street"},
            {"time": "14:00", "description": "Explore the British Museum", "location": "Great Russell Street"},
            {"time": "18:00", "description": "Dinner at The Ivy", "location": "1-5 West Street"},
            {"time": "10:00", "description": "Visit Buckingham Palace", "location": "Westminster"},
            {"time": "13:00", "description": "Lunch at Dishoom", "location": "12 Upper St Martin's Lane"},
            {"time": "15:00", "description": "Ride the London Eye", "location": "Riverside Building, County Hall"},
            {"time": "19:00", "description": "Dinner and show in West End", "location": "Shaftesbury Avenue"},
            {"time": "09:30", "description": "Visit Westminster Abbey", "location": "20 Deans Yard"},
            {"time": "12:00", "description": "Lunch at Sketch", "location": "9 Conduit Street"},
            {"time": "14:00", "description": "Explore Tate Modern", "location": "Bankside"},
            {"time": "18:30", "description": "Dinner at Rules", "location": "35 Maiden Lane"}
        ]
    }
    
    # Default activities for any city
    default_activities = [
        {"time": "09:00", "description": f"Visit {request.city} Historical Museum", "location": "City Center"},
        {"time": "12:30", "description": "Lunch at Local Restaurant", "location": "Main Square"},
        {"time": "14:00", "description": "City Sightseeing Tour", "location": "Tourist Information Center"},
        {"time": "18:00", "description": "Dinner at Popular Restaurant", "location": "Downtown"},
        {"time": "10:00", "description": "Visit Local Market", "location": "Market Square"},
        {"time": "13:00", "description": "Lunch at Café", "location": "Shopping District"},
        {"time": "15:00", "description": "Explore City Park", "location": "Central Park"},
        {"time": "19:00", "description": "Dinner and Cultural Show", "location": "Entertainment District"},
        {"time": "09:30", "description": "Visit Art Gallery", "location": "Cultural District"},
        {"time": "12:00", "description": "Street Food Experience", "location": "Food Street"},
        {"time": "14:30", "description": "Shopping at Local Boutiques", "location": "Shopping Street"},
        {"time": "18:30", "description": "Sunset Dinner", "location": "Scenic Viewpoint"}
    ]
    
    # Get activities for the city (case insensitive)
    city_lower = request.city.lower()
    activities = city_activities.get(city_lower, default_activities)
    
    # Create itinerary
    itinerary = []
    for day in range(1, duration + 1):
        current_date = start_date + timedelta(days=day-1)
        date_str = current_date.strftime("%Y-%m-%d")
        
        # Select activities for this day (4 activities per day)
        day_activities = []
        for i in range(4):
            activity_index = (day - 1) * 4 + i
            if activity_index < len(activities):
                day_activities.append(activities[activity_index])
            else:
                # Cycle through activities if we run out
                day_activities.append(activities[activity_index % len(activities)])
        
        itinerary.append({
            "day": day,
            "date": date_str,
            "activities": day_activities
        })
    
    return {"itinerary": itinerary}

@app.post("/api/locations/suggest")
async def suggest_locations(request: LocationRequest):
    try:
        # Check if GROQ_API is available and validated
        if not GROQ_API_AVAILABLE:
            print("Warning: GROQ_API not available. Using fallback locations.")
            return get_fallback_locations(request.city)
            
        # Initialize the LLM
        groq_api_key = os.environ.get("GROQ_API_KEY")
        llm = ChatGroq(
            temperature=0.2,
            api_key=groq_api_key,
            model_name="llama-3.3-70b-versatile"
        )
        
        # Create the prompt
        prompt_text = f"Suggest 5 famous tourist locations in {request.city}"
        if request.query:
            prompt_text += f" related to {request.query}"
        
        # Generate suggestions
        print(f"Generating location suggestions for {request.city}")
        response = llm.invoke(prompt_text)
        
        # Parse the response to extract locations
        locations = []
        for line in response.content.split("\n"):
            if line.strip().startswith("-") or line.strip().startswith("*"):
                locations.append(line.strip()[1:].strip())
        
        # If no locations were found, provide a fallback
        if not locations:
            print("No locations found in API response. Using fallback.")
            return get_fallback_locations(request.city)
        
        # Get coordinates for each location
        locations_with_coords = []
        for location in locations[:5]:  # Limit to 5 locations
            full_location = f"{location}, {request.city}"
            coords = get_location_coordinates(full_location)
            locations_with_coords.append({
                "name": location,
                "latitude": coords["latitude"],
                "longitude": coords["longitude"]
            })
        
        print(f"Successfully generated {len(locations_with_coords)} location suggestions")
        return {"locations": locations_with_coords}
    except Exception as e:
        print(f"Error suggesting locations: {str(e)}")
        return get_fallback_locations(request.city)

def get_fallback_locations(city):
    """Provide fallback locations when API calls fail"""
    # Popular landmarks for common cities
    city_landmarks = {
        "paris": ["Eiffel Tower", "Louvre Museum", "Notre-Dame Cathedral", "Arc de Triomphe", "Montmartre"],
        "london": ["Big Ben", "Tower of London", "Buckingham Palace", "London Eye", "British Museum"],
        "new york": ["Times Square", "Central Park", "Empire State Building", "Statue of Liberty", "Brooklyn Bridge"],
        "tokyo": ["Tokyo Tower", "Senso-ji Temple", "Shibuya Crossing", "Meiji Shrine", "Tokyo Skytree"],
        "rome": ["Colosseum", "Vatican City", "Trevi Fountain", "Roman Forum", "Pantheon"],
        "sydney": ["Sydney Opera House", "Sydney Harbour Bridge", "Bondi Beach", "Taronga Zoo", "Royal Botanic Garden"],
        "dubai": ["Burj Khalifa", "Palm Jumeirah", "Dubai Mall", "Burj Al Arab", "Dubai Creek"],
        "bangkok": ["Grand Palace", "Wat Arun", "Chatuchak Market", "Wat Pho", "Khao San Road"],
        "barcelona": ["Sagrada Familia", "Park Güell", "Casa Batlló", "La Rambla", "Gothic Quarter"],
        "istanbul": ["Hagia Sophia", "Blue Mosque", "Topkapi Palace", "Grand Bazaar", "Bosphorus"]
    }
    
    # Default landmarks for any city
    default_landmarks = ["City Center", "Main Square", "Historical Museum", "Central Park", "Local Market"]
    
    # Get landmarks for the city (case insensitive)
    city_lower = city.lower()
    landmarks = city_landmarks.get(city_lower, default_landmarks)
    
    # Get coordinates for each location
    locations_with_coords = []
    for landmark in landmarks:
        full_location = f"{landmark}, {city}"
        coords = get_location_coordinates(full_location)
        locations_with_coords.append({
            "name": landmark,
            "latitude": coords["latitude"],
            "longitude": coords["longitude"]
        })
    
    return {"locations": locations_with_coords}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
