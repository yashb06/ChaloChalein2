import streamlit as st
import folium
from streamlit_folium import folium_static

def show_map(locations):
    """
    Display an interactive map with the given locations
    locations: List of dictionaries containing location information
    """
    # Create a map centered on the first location
    first_loc = locations[0]
    m = folium.Map(
        location=[first_loc['coordinates'].split(',')[0], 
                 first_loc['coordinates'].split(',')[1]],
        zoom_start=13
    )
    
    # Add markers for each location
    for loc in locations:
        lat, lng = loc['coordinates'].split(',')
        folium.Marker(
            [float(lat), float(lng)],
            popup=loc['location'],
            tooltip=loc['activity']
        ).add_to(m)
    
    # Display the map
    folium_static(m)
