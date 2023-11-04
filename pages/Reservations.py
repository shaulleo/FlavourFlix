import streamlit as st
import pandas as pd
from functions.streamlitfunc import *

data = pd.read_csv('/Users/madalena.frango/Desktop/capstone/FlavourFlix/data/all_thefork_scrapes.csv')

def reservations_page():
    st.title("Reservations Page")
    st.write("View and manage your reservations here.")

    

    if 'selected_restaurant' not in st.session_state:
        selected_restaurant = st.session_state.selected_restaurant = None
    else:
        selected_restaurant = st.session_state.selected_restaurant
    # Retrieve the selected restaurant from session state
    

    # If the user has not selected a restaurant yet, show a selectbox
    if selected_restaurant is None:
        # Get a list of all the restaurants
        restaurants = data['name'].unique().tolist()
        # Add an option for no selection
        restaurants = [""] + restaurants
        # Create a selectbox for the user to choose a restaurant
        selected_restaurant = st.selectbox("Select Restaurant", restaurants)
        # Store the selected restaurant in session state
        st.session_state.selected_restaurant = selected_restaurant
    else:
        # select in the select box the restaurant that was selected before
        selected_restaurant = st.selectbox("Select Restaurant", [selected_restaurant])

    reservation_date = st.date_input('Reservation Date')
    reservation_time = st.time_input('Reservation Time')

# Usage: Call the function to show the reservations page
reservations_page()