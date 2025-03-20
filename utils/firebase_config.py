import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st

def initialize_firebase():
    """
    Initialize Firebase with credentials
    """
    if not firebase_admin._apps:
        cred = credentials.Certificate(st.secrets["FIREBASE_CREDENTIALS"])
        firebase_admin.initialize_app(cred)
    
    return firestore.client()

def save_trip(user_email, trip_data):
    """
    Save trip data to Firestore
    """
    db = initialize_firebase()
    trips_ref = db.collection('trips')
    
    trips_ref.add({
        'user_email': user_email,
        'trip_data': trip_data,
        'created_at': firestore.SERVER_TIMESTAMP
    })

def get_user_trips(user_email):
    """
    Retrieve all trips for a user
    """
    db = initialize_firebase()
    trips_ref = db.collection('trips')
    
    trips = trips_ref.where('user_email', '==', user_email).get()
    return [trip.to_dict() for trip in trips]
