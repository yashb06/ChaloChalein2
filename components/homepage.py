import streamlit as st

def show_homepage():
    st.title("✈️ AI Travel Planner")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Plan Your Perfect Trip with AI
        Let our AI-powered travel planner help you create the perfect itinerary!
        
        - 🤖 Chat with our AI to plan your trip
        - 🗺️ Get personalized recommendations
        - 🌤️ Check weather forecasts
        - 📍 Explore interactive maps
        """)
        
        if not st.session_state.user:
            col3, col4 = st.columns(2)
            with col3:
                st.button("Login", on_click=lambda: setattr(st.session_state, 'page', 'auth'))
            with col4:
                st.button("Sign Up", on_click=lambda: setattr(st.session_state, 'page', 'auth'))
        else:
            st.button("Start Planning", on_click=lambda: setattr(st.session_state, 'page', 'chatbot'))
    
    with col2:
        st.image("https://your-travel-image-url.jpg", use_column_width=True)