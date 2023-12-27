
import streamlit as st
import pandas as pd
import ast
import numpy as np
import json
from functions.streamlitfunc import *
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.stylable_container import stylable_container
from streamlit_carousel import carousel


st.set_page_config(page_title='Restaurant', page_icon="ext_images\page_icon.png", layout="wide", initial_sidebar_state="collapsed")
data = pd.read_csv('data/preprocessed_data.csv')



def find_res_photos(restaurant):
    data_with_photos = pd.read_csv('data/alltheforkscrapes2.csv')
    photo_columns = [col for col in list(data_with_photos.columns) if 'photos' in col]
    photo_columns.append('name')
    data_with_photos = data_with_photos[photo_columns]
    res_photos = data_with_photos[data_with_photos['name'] == restaurant]
    res_photos = res_photos.dropna(axis=1, how='all')
    images = []
    photo_columns = [col for col in list(res_photos.columns) if 'photos' in col]
    for col in photo_columns:
        image_info = dict(title = '',
                          text = f'{res_photos["name"].values[0]}',
                          img = res_photos[col].values[0])
        images.append(image_info)
    
    return images


def show_menu(restaurant):
    if type(restaurant['menu_pre_proc'].iloc[0]) == str:
        menu = restaurant['menu_pre_proc'].iloc[0]
        menu = menu.replace('"{', '{')
        menu = menu.replace('}"', '}')
        menu = menu.replace("::", ":")
        menu = menu.replace('""', '"')
        menu = ast.literal_eval(menu)  

        menu_items = {}

        for section, dishes in menu.items():
            for dish, details in dishes.items():
                if section not in menu_items:
                    menu_items[section] = {}
                menu_items[section][dish] = details
    else: 
        menu_items = None
        menu = 'Not Available'
        
    with st.expander("Check out the Menu!"):
        if menu_items is not None:
            for section, dishes in menu_items.items():
                st.markdown(f"###### {section}:")
                for dish, details in dishes.items():
                    price = details['price'] if details['price'] else "Price Unavailable"
                    description = details['description'] if details['description'] != 'null' else ""
                        
                    if description:
                        st.markdown(f" - <p> {dish}: {price} € <small> ({description}) </small> </p> ", unsafe_allow_html=True)
                    else:
                        st.markdown(f"- {dish}: {price} €")
        else:
            st.markdown('Sorry! It seems that the restaurant did\nnot make their menu available yet... :disappointed:')


def show_schedule(restaurant):
    with st.expander("View Restaurant Schedule"):
        if restaurant['schedule'].iloc[0] == 'Not Available':
            st.markdown('Sorry! It seems that the restaurant did\nnot make their schedule available yet... :disappointed:')
        else:
            schedule = ast.literal_eval(restaurant['schedule'].iloc[0])
            for day, hours in schedule.items():
                st.markdown(f"###### {day}:")
                st.markdown(f" - {hours}")


def show_time_away(restaurant):
    if 'authentication_status' in st.session_state and st.session_state['authentication_status'] == True:
        if 'username'  in st.session_state and 'email' in st.session_state:
            clients = pd.read_csv('data/clientDataClean.csv')
            current_client = clients[clients['email'] == st.session_state['email']].iloc[0]
            prefers_driving = current_client['travel_car']
            if "current_location" in st.session_state and st.session_state.current_location != False:
                if prefers_driving:
                    by_car = st.session_state.current_location.getDirections(restaurant['latitude'].iloc[0], restaurant['longitude'].iloc[0], ['driving'])
                    distance = f'{by_car["driving"].meters} meters' if by_car['driving'].meters < 1000 else f"{by_car['driving'].km} km"
                    time_away = f"{by_car['driving'].minutes}min away" if by_car['driving'].minutes < 60 else f"{by_car['driving'].hours} away"
                    st.markdown(f"🚗 **{distance}** ({time_away})")
                else:
                    by_foot = st.session_state.current_location.getDirections(restaurant['latitude'].iloc[0], restaurant['longitude'].iloc[0], ['walking'])
                    distance = f'{by_foot["walking"].meters} meters' if by_foot['walking'].meters < 1000 else f"{by_foot['walking'].km} km"
                    time_away = f"{by_foot['walking'].minutes}min away" if by_foot['walking'].minutes < 60 else f"{by_foot['walking'].hours} away"
                    st.markdown(f"🚶 **{distance}** ({time_away})")
            else:
                st.markdown('')
        else:
            st.markdown('')
    else:
        st.markdown('')
        

def restaurant_details():

    food_rating = data.loc[data['name'] == selected_restaurant, 'foodRatingSummary'].iloc[0]
    service_rating = data.loc[data['name'] == selected_restaurant, 'serviceRatingSummary'].iloc[0]
    ambience_rating = data.loc[data['name'] == selected_restaurant, 'ambienceRatingSummary'].iloc[0]
    michelin_value = data.loc[data['name'] == selected_restaurant,'michelin'].iloc[0]
    max_party_size = data.loc[data['name'] == selected_restaurant, 'maxPartySize'].iloc[0]
    outdoor_area = data.loc[data['name'] == selected_restaurant,'outdoor_area'].iloc[0]


    st.markdown(f"<h1 style='text-align: center; color: black;'>{selected_restaurant}</h1>", unsafe_allow_html=True)

    st.markdown('<br>', unsafe_allow_html=True)
    m1, m2, m3, m4, m5 = st.columns([1,1,1, 1, 1])
    with m1:
        if np.isnan(food_rating):
            food_rating = 'Not Available'
        else:
            food_rating = f'{np.round(food_rating, 2)}/10.0'
        with stylable_container(
        key="container_with_border",
        css_styles="""
            {
                border: 1px solid rgba(49, 51, 63, 0.2);
                border-radius: 0.5rem;
                padding: calc(1em - 1px)
            }
            """):
            st.metric(label = '🍲 Food Rating', value = f"{food_rating}")

    with m2:
        if np.isnan(service_rating):
            service_rating = 'Not Available'
        else:
            service_rating = f'{np.round(service_rating,2)}/10.0'
    
        with stylable_container(
        key="container_with_border",
        css_styles="""
            {
                border: 1px solid rgba(49, 51, 63, 0.2);
                border-radius: 0.5rem;
                padding: calc(1em - 1px)
            }
            """    ):
            st.metric(label = '👨‍🍳 Service Rating', value = f"{service_rating}")

    with m4:
        if np.isnan(max_party_size):
            max_party_size = 'Not Available'
        else:
            max_party_size = int(max_party_size)
        with stylable_container(
        key="container_with_border",
        css_styles="""
            {
                border: 1px solid rgba(49, 51, 63, 0.2);
                border-radius: 0.5rem;
                padding: calc(1em - 1px)
            }
            """,    ):
            st.metric(label = '🧑🏽‍🤝‍🧑🏿 Maximum Party Size', value = max_party_size)
    
    with m3:
        if np.isnan(ambience_rating):
            ambience_rating = 'Not Available'
        else:
            ambience_rating = f'{np.round(ambience_rating,2)}/10.0'

        if michelin_value == 1:
            michelin_score = 'Michelin ⭐' if michelin_value == 1 else 'None'
            with stylable_container(
            key="container_with_border",
            css_styles="""
                {
                    border: 1px solid rgba(49, 51, 63, 0.2);
                    border-radius: 0.5rem;
                    padding: calc(1em - 1px)
                    align-items: center;
                }
                """,
        ):
                st.metric(label= 'Awarded with', value=michelin_score)
        else:
            with stylable_container(
            key="container_with_border",
            css_styles="""
                {
                    border: 1px solid rgba(49, 51, 63, 0.2);
                    border-radius: 0.5rem;
                    padding: calc(1em - 1px)
                    align-items: center;
                }
                """,
        ):
                st.metric(label= '🏙️ Ambience Rating', value=f'{ambience_rating}')

    with m5:
        if outdoor_area == 1:
            outdoor_area = 'Yes'
        else:
            outdoor_area = 'No'
        with stylable_container(
        key="container_with_border",
        css_styles="""
            {
                border: 1px solid rgba(49, 51, 63, 0.2);
                border-radius: 0.5rem;
                padding: calc(1em - 1px)
                align-items: center;
            }
            """,
    ):
            st.metric(label= '🏖️ Outdoor Area', value=outdoor_area)

    # style_metric_cards(border_left_color='#FFFFFF', box_shadow=False)
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    col1, col2 = st.columns([3,3], gap = 'large')
    with col1:
        images = find_res_photos(selected_restaurant)
        carousel(items=images, width=1.15)

    with col2:
        with stylable_container(
        key="container_with_border",
        css_styles="""
            {
                border: 1px solid rgba(49, 51, 63, 0.2);
                border-radius: 0.5rem;
                padding: calc(1em - 1px)
                text-align: left
            }
            """,
    ):
            st.markdown(f"**Address:** {data.loc[data['name'] == selected_restaurant, 'address'].iloc[0]}")
            st.markdown(f"**Phone:** {data.loc[data['name'] == selected_restaurant, 'phone'].iloc[0]}")
            st.markdown(f"**Cuisine:** {data.loc[data['name'] == selected_restaurant, 'cuisine'].iloc[0]}")
            st.markdown(f"**Style:** {data.loc[data['name'] == selected_restaurant,'style'].iloc[0]}")
            st.markdown(f"**Average Price:** {data.loc[data['name'] == selected_restaurant, 'averagePrice'].iloc[0]}€")
            show_time_away(data.loc[data['name'] == selected_restaurant])
            if st.button(f"Reserve Now!"):
                st.session_state.selected_restaurant = selected_restaurant
                nav_page("Reservations")
    show_menu(data.loc[data['name'] == selected_restaurant])
    show_schedule(data.loc[data['name'] == selected_restaurant])
    

if 'selected_restaurant' not in st.session_state:
    selected_restaurant = st.session_state.selected_restaurant = None
else:
    selected_restaurant = st.session_state.selected_restaurant

    

    # If the user has not selected a restaurant yet, show a selectbox
if selected_restaurant is None:
    # Get a list of all the restaurants
    restaurants = ["Search"] + data['name'].unique().tolist()
    # Create a selectbox for the user to choose a restaurant
    selected = st.selectbox("Select Restaurant", restaurants)
    if selected != "Search":
        selected_restaurant = data.loc[data['name'] == selected, 'name'].iloc[0]
    # Store the selected restaurant in session state
        st.session_state.selected_restaurant = selected_restaurant
        restaurant_details()
    

    else:
        st.write("Please select a restaurant from the list above :)")


    
else:
    # select in the select box the restaurant that was selected before
    #selected_restaurant = st.selectbox("Select Restaurant", [selected_restaurant])
    restaurant_details()

