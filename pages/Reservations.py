import streamlit as st
import pandas as pd
import time
from functions.streamlitfunc import *
from functions.utils import *
from datetime import date
from streamlit_extras.switch_page_button import switch_page 


client_data = pd.read_csv('data/clientDataClean.csv')
res_data = pd.read_csv('data/preprocessed_data.csv')
#st.set_page_config(page_title='Restaurant', page_icon="ext_images\page_icon.png", layout="wide", initial_sidebar_state="collapsed")

def confirm_reservation():
    st.markdown(f':white_check_mark: Your reservation has been confirmed! \nYou will receive a confirmation email shortly.')
    user_info = client_data[client_data['email'] == st.session_state['email']]
    st.markdown(f'**Reservation Details:**\n\n**Name**: {user_info["first_name"].values[0]} {user_info["last_name"].values[0]} **\n**Restaurant:** {st.session_state.selected_restaurant}\n**Date:** {st.session_state.reservation_date}\n**Time:** {st.session_state.reservation_time}\n**Number of People:** {st.session_state["num_people"]}\n**Special Requests:** {st.session_state.special_requests}')


def verify_reservation(restaurant, reservation_date, reservation_time):
    restaurant_schedule = res_data[res_data['name'] == restaurant]['schedule'].values[0]
    availability = check_if_open(restaurant_schedule, reservation_date, reservation_time)
    if availability == 'Open':
        confirm_reservation()
    elif availability == 'Closed':
        st.markdown(f'Ups! Unfortunately {restaurant} is closed on {reservation_date} at {reservation_time}.\nPlease try another date. Thankyou.')
        ##### LIMPAR OS FIELDS
    else:
        st.markdown(f'Ups! Unfortunately we do not have information about the schedule of {restaurant} on {reservation_date}.\nPlease try contacting them directly. Thankyou.')
        switch_page('restaurant')






def reservations_page():
    st.title("Reserve Now!")
    st.write("View and manage your reservations here.")

    if 'selected_restaurant' not in st.session_state:
        selected_restaurant = st.session_state.selected_restaurant = None
    else:
        selected_restaurant = st.session_state.selected_restaurant
    # Retrieve the selected restaurant from session state
    

    # If the user has not selected a restaurant yet, show a selectbox
    if selected_restaurant is None:
        # Get a list of all the restaurants
        restaurants = res_data['name'].unique().tolist()
        # Add an option for no selection
        restaurants = [""] + restaurants
        # Create a selectbox for the user to choose a restaurant
        selected_restaurant = st.selectbox("Select Restaurant", restaurants)
        # Store the selected restaurant in session state
        st.session_state.selected_restaurant = selected_restaurant
    else:
        # select in the select box the restaurant that was selected before
        selected_restaurant = st.selectbox("Select Restaurant", [selected_restaurant])

    res_info = res_data[res_data['name'] == selected_restaurant]
    max_party_size = res_info['maxPartySize'].values[0]
    if np.isnan(max_party_size):
        max_party_size = 20
    else:
        max_party_size = int(max_party_size)

    reservation_date = st.date_input('Reservation Date')
    st.session_state.reservation_date = reservation_date
    reservation_time = st.time_input('Reservation Time')
    st.session_state.reservation_time = reservation_time
    num_people = st.number_input('Number of People', min_value=1, max_value=max_party_size, value=1)
    st.session_state.num_people = num_people
    special_requests = st.text_input('Any Special Requests?')
    st.session_state.special_requests = special_requests


    col1, col2 = st.columns(2)
    with col1:
        confirm_res = st.button("Confirm Reservation", key='confirm_res')
        if confirm_res:
            verify_reservation(selected_restaurant, reservation_date, reservation_time)
            # switch_page("restaurant")

    with col2:
        continue_searching = st.button("Continue Searching", key='continue_searching')
        if continue_searching:
            switch_page("Search")



if ('authentication_status' in st.session_state) and (st.session_state['authentication_status'] == True) and ('username' in st.session_state) and ('email' in st.session_state):
    pages_logged_in()
    reservations_page()

else:
    pages_logged_off()
    st.error('Ups! Something went wrong. Please try login again.', icon='🚨')
    st.session_state['authentication_status'] = False
    st.write('You need to be logged in to access this feature.')
    with st.spinner('Redirecting you to the Login page...'):
        time.sleep(3)
    switch_page('log in')