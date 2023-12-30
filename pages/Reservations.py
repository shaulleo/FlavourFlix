import streamlit as st
import pandas as pd
import time
from functions.streamlitfunc import *
from functions.utils import *
from datetime import date
import folium
from streamlit_folium import st_folium
from streamlit_extras.switch_page_button import switch_page 
from streamlit_extras.stylable_container import stylable_container


if 'reserve' not in st.session_state:
    st.session_state.reserve = False
if 'run' not in st.session_state:
    st.session_state.run = 0
if 'reservation_name' not in st.session_state:
    st.session_state.reservation_name = None
if 'reservation_date' not in st.session_state:
    st.session_state.reservation_date = None
if 'reservation_time' not in st.session_state:
    st.session_state.reservation_time = None
if 'num_people' not in st.session_state:
    st.session_state.num_people = 1
if 'special_requests' not in st.session_state:
    st.session_state.special_requests = None
if 'selected_restaurant' not in st.session_state:
    st.session_state.selected_restaurant = None


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
            rest_image = restaurants[restaurants['name'] == reservation[1]["res_name"]]['photo'].values[0]
            st.image(rest_image, width=200)
        with col2:
            st.markdown(f'**Restaurant**: {reservation[1]["res_name"]}')
            st.markdown(f'**Guest Name**: {reservation[1]["guest_name"]}')
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
    else:
        st.markdown("You don't have any reservations yet. Search for a restaurant and make a reservation now!")
        with st.spinner('Redirecting you to the Search page...'):
            time.sleep(3)
        switch_page('Search')


def save_reservation():
    reservations = pd.read_csv('data/reservations.csv')
    new_res = pd.DataFrame({
        'email': [st.session_state['email']],
        'guest_name': [st.session_state['reservation_name']],
        'res_name': [st.session_state['selected_restaurant']],
        'date': [st.session_state['reservation_date']],
        'time': [st.session_state['reservation_time']],
        'num_people': [st.session_state['num_people']],
        'special_requests': [st.session_state['special_requests']]
    })
    reservations = pd.concat([reservations, new_res], ignore_index=True)
    reservations.to_csv('data/reservations.csv', index=False)
    

def click_reserve():
    st.session_state.run += 1
    verify_reservation(st.session_state['selected_restaurant'],
                        st.session_state['reservation_date'], st.session_state['reservation_time'])

def reservation_state(status):
    if status == 'Open':
        return False
    else:
        return True

def verify_reservation(restaurant, reservation_date, reservation_time):
    restaurants = pd.read_csv('data/preprocessed_data.csv')
    restaurant_schedule = restaurants[restaurants['name'] == restaurant]['schedule'].values[0]
    availability = check_if_open(restaurant_schedule, reservation_date, reservation_time)
    if availability == 'Open':
        st.markdown(f':white_check_mark: Your reservation has been confirmed! \nYou will receive a confirmation email shortly.')
        save_reservation()
    elif availability == 'Closed':
        st.error(f'Ups! Unfortunately {restaurant} is closed on {reservation_date} at {reservation_time}.\n Please try another date. Thankyou.')
    else:
        st.error(f'Ups! Unfortunately we do not have information about the schedule of {restaurant} on {reservation_date}.\nPlease try contacting them directly. Thankyou.')
    st.session_state['reserve'] = reservation_state(availability)


def fill_reservation():
    restaurants = pd.read_csv('data/preprocessed_data.csv')
    col1, col2 = st.columns(2, gap='large')
    with col1:
        with stylable_container(
            key="container_with_border",
                    css_styles="""
                {
                    border: 0px solid rgb(36, 36, 37);
                    background-color: #FFFFFF;
                    padding: calc(1em - 1px);
                    text-align: justify;
                    width: 90%;
                }
            """,
        ):
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
            else:
                st.write("Something went wrong. Please try again.")
                st.session_state['reserve'] = True
            restaurant_info = restaurants[restaurants['name'] == selected_restaurant]
            max_party_size = restaurant_info['maxPartySize'].values[0]
            if np.isnan(max_party_size):
                max_party_size = 20
            else:
                max_party_size = int(max_party_size)

            reservation_name = st.text_input('Reservation Name', value=st.session_state['reservation_name'])
            st.session_state.reservation_name = reservation_name
            reservation_date = st.date_input('Reservation Date',  min_value=date.today(), value=st.session_state['reservation_date'])
            st.session_state.reservation_date = reservation_date
            reservation_time = st.time_input('Reservation Time', value=st.session_state['reservation_time'])
            st.session_state.reservation_time = reservation_time
            num_people = st.number_input('Number of People', min_value=1, max_value=max_party_size, value=st.session_state['num_people'])
            st.session_state.num_people = num_people
            special_requests = st.text_input('Any Special Requests?', value=st.session_state['special_requests'], max_chars=500, placeholder='Feel free to ask for any special elements to your reservation.')
            st.session_state.special_requests = special_requests
    with col2:
        if 'selected_restaurant' not in st.session_state or st.session_state['selected_restaurant'] is None:
            st.write('')
        else:
            st.write('')
            st.write('')
            latitude = restaurant_info['latitude'].values[0]
            longitude = restaurant_info['longitude'].values[0]
            m = folium.Map(location=(latitude, longitude), zoom_start=12, tiles="OpenStreetMap")
            folium.Marker(location=(latitude, longitude), popup=selected_restaurant).add_to(m)
            st_folium(m, height=300, width=600, returned_objects=[])
            st.caption("""Note that the pin presented on the map is not the exact location of the restaurant, but rather an estimation.""", unsafe_allow_html=True)
            st.write('')
            show_schedule(restaurant_info)



if ('authentication_status' in st.session_state) and (st.session_state['authentication_status'] == True) and ('username' in st.session_state) and ('email' in st.session_state):
    pages_logged_in()
    if st.session_state['reserve']: 
        fill_reservation()
        col1, col2 = st.columns(2)
        with col1:
            st.button("Reserve", key=f'confirm_reservation_{st.session_state["run"]}', on_click = click_reserve)
        st.session_state['run'] += 1
    elif not st.session_state['reserve']: 
        show_all_reservations()
        st.session_state['run'] += 1
    else:
        st.write("Something went wrong. Please try again.")
        st.session_state['run'] += 1
        st.session_state['reserve'] = True

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