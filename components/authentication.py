import streamlit as st
import firebase_admin
from firebase_admin import auth

def show_auth_page():
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        st.header("Login")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login"):
            try:
                user = auth.get_user_by_email(email)
                # In production, use proper password verification
                st.session_state.user = {"email": email}
                st.session_state.page = 'home'
                st.rerun()
            except:
                st.error("Invalid credentials")
    
    with tab2:
        st.header("Sign Up")
        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        if st.button("Sign Up"):
            if password != confirm_password:
                st.error("Passwords don't match")
            else:
                try:
                    user = auth.create_user(
                        email=email,
                        password=password
                    )
                    st.success("Account created successfully!")
                    st.session_state.user = {"email": email}
                    st.session_state.page = 'home'
                    st.rerun()
                except:
                    st.error("Error creating account")