import streamlit as st
import pandas as pd
import time
from functions.streamlitfunc import *
from functions.utils import *
from datetime import date
from streamlit_extras.switch_page_button import switch_page 
from streamlit_extras.stylable_container import stylable_container


if 'reserve' not in st.session_state:
    st.session_state.reserve = False
if 'run' not in st.session_state:
    st.session_state.run = 0
if 'verify_reservation1' not in st.session_state:
    st.session_state.verify_reservation1 = False


def display_reservation_card(reservation):
    restaurants = pd.read_csv('data/preprocessed_data.csv')
    with stylable_container(key="container_with_border",
            css_styles="""
                {
                    border: 1px solid rgba(49, 51, 63, 0.2);
                    border-radius: 0.5rem;
                    padding: calc(1em - 1px);
                    text-align: justify;
                }                """,):
        col1, col2 = st.columns([0.3, 0.7])
        with col1:
            rest_image = restaurants[restaurants['name'] == reservation[1]["restaurant"]]['photo'].values[0]
            st.image(rest_image, width=200)
        with col2:
            st.markdown(f'**Restaurant**: {reservation[1]["restaurant"]}')
            st.markdown(f'**Date**: {reservation[1]["date"]}')
            st.markdown(f'**Time**: {reservation[1]["time"]}')
            st.markdown(f'**Number of People**: {reservation[1]["num_people"]}')
            st.markdown(f'**Special Requests**: {reservation[1]["special_requests"]}')


def show_all_reservations():
    reservations = pd.read_csv('data/reservations.csv')
    if st.session_state['email'] in reservations['email'].values:
        user_res = reservations[reservations['email'] == st.session_state['email']]
        if len(user_res) == 0:
            st.markdown("You don't have any reservations yet. Search for a restaurant and make a reservation now!")
            with st.spinner('Redirecting you to the Search page...'):
                time.sleep(3)
            switch_page('Search')
        else:
            st.markdown(f'**Your Reservations**')
            for reservation in user_res.iterrows():
                display_reservation_card(reservation)


def save_reservation():
    reservations = pd.read_csv('data/reservations.csv')
    new_res = pd.DataFrame({
        'email': [st.session_state['email']],
        'restaurant': [st.session_state['selected_restaurant']],
        'date': [st.session_state['reservation_date']],
        'time': [st.session_state['reservation_time']],
        'num_people': [st.session_state['num_people']],
        'special_requests': [st.session_state['special_requests']]
    })
    reservations = pd.concat([reservations, new_res], ignore_index=True)
    reservations.to_csv('data/reservations.csv', index=False)
    

def click_reserve():
    st.session_state.verify_reservation1 = True
    st.session_state.run += 1
    verify_reservation(st.session_state['selected_restaurant'],
                        st.session_state['reservation_date'], st.session_state['reservation_time'])
    #st.session_state.verify_reservation1 = False


def verify_reservation(restaurant, reservation_date, reservation_time):
    restaurants = pd.read_csv('data/preprocessed_data.csv')
    restaurant_schedule = restaurants[restaurants['name'] == restaurant]['schedule'].values[0]
    availability = check_if_open(restaurant_schedule, reservation_date, reservation_time)
    if availability == 'Open':
        st.markdown(f':white_check_mark: Your reservation has been confirmed! \nYou will receive a confirmation email shortly.')
        save_reservation()
        st.session_state['verify_reservation1'] = False  
        st.session_state['reserve'] = False
    elif availability == 'Closed':
        st.markdown(f'Ups! Unfortunately {restaurant} is closed on {reservation_date} at {reservation_time}.\n Please try another date. Thankyou.')
        st.session_state['verify_reservation1'] = False  
        st.session_state['reserve'] = True
    else:
        st.markdown(f'Ups! Unfortunately we do not have information about the schedule of {restaurant} on {reservation_date}.\nPlease try contacting them directly. Thankyou.')
        st.session_state['verify_reservation1'] = False  
        st.session_state['reserve'] = True


def fill_reservation():
    restaurants = pd.read_csv('data/preprocessed_data.csv')
    st.title("Reserve Now!")
    if 'selected_restaurant' not in st.session_state or st.session_state['selected_restaurant'] is None:
        # Get a list of all the restaurants
        restaurants = restaurants['name'].unique().tolist()
        # Add an option for no selection
        restaurants = [""] + restaurants
        # Create a selectbox for the user to choose a restaurant
        selected_restaurant = st.selectbox("Select Restaurant", restaurants)
        # Store the selected restaurant in session state
        st.session_state.selected_restaurant = selected_restaurant
    elif st.session_state['selected_restaurant'] is not None:
        st.markdown(f'**Reserve for restaurant**: {st.session_state["selected_restaurant"]}')
        selected_restaurant = st.session_state['selected_restaurant']

    restaurant_info = restaurants[restaurants['name'] == selected_restaurant]
    max_party_size = restaurant_info['maxPartySize'].values[0]
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
    



if ('authentication_status' in st.session_state) and (st.session_state['authentication_status'] == True) and ('username' in st.session_state) and ('email' in st.session_state):
    pages_logged_in()
    header_image = "ext_images/logo1.jpeg"
    st.image(header_image, width=500)
    st.divider()
    if st.session_state['reserve'] and not st.session_state['verify_reservation1']:
        fill_reservation()
        col1, col2 = st.columns(2)
        with col1:
            st.button("Reserve", key=f'confirm_reservation_{st.session_state["run"]}', on_click = click_reserve)
    elif not st.session_state['reserve'] and not st.session_state['verify_reservation1']:
        show_all_reservations()
    else:
        st.write("Something went wrong. Please try again.")
        st.session_state['reserve'] = True
        st.session_state['verify_reservation1'] = False
    col1, col2 = st.columns(2)
    with col2:
        continue_searching = st.button("Continue Searching", key=f'continue_searching_1')
        if continue_searching:
            switch_page("Search")

else:
    pages_logged_off()
    st.error('Ups! Something went wrong. Please try login again.', icon='🚨')
    st.session_state['authentication_status'] = False
    st.write('You need to be logged in to access this feature.')
    with st.spinner('Redirecting you to the Login page...'):
        time.sleep(3)
    switch_page('log in')