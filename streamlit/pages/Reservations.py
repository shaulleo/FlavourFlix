import streamlit as st
import pandas as pd

data = pd.read_csv('/Users/madalena.frango/Desktop/capstone/FlavourFlix/data/all_thefork_scrapes.csv')

st.title("Reservations Page")
st.write("View and manage your reservations here.")
restaurant_names = data['name'].tolist()
# Create a custom list with "Search" at the beginning and append the restaurant names
custom_list = [" "] + restaurant_names
# Create a selectbox with the custom list
selected_restaurant = st.selectbox('Select a restaurant', custom_list)
reservation_date = st.date_input('Reservation Date')
reservation_time = st.time_input('Reservation Time')