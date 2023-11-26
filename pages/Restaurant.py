
import streamlit as st
import pandas as pd
import ast
import json
from functions.streamlitfunc import *
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.stylable_container import stylable_container



st.set_page_config(page_title='Restaurant', page_icon="ext_images\page_icon.png", layout="wide", initial_sidebar_state="collapsed")
data = pd.read_csv('data/preprocessed_data.csv')
st.title("Restaurant's Details")

def restaurant_details():

    st.markdown(f"<h1 style='text-align: center; color: black;'>{selected_restaurant}</h1>", unsafe_allow_html=True)

    st.markdown('<br>', unsafe_allow_html=True)
    m1, m2, m3, m4, m5 = st.columns([1,1,1, 1, 1])
    with m1:
        with stylable_container(
        key="container_with_border",
        css_styles="""
            {
                border: 1px solid rgba(49, 51, 63, 0.2);
                border-radius: 0.5rem;
                padding: calc(1em - 1px)
            }
            """,
    ):
            st.metric(label = 'Food Rating', value = data.loc[data['name'] == selected_restaurant, 'foodRatingSummary'].iloc[0])
    with m2:
        with stylable_container(
        key="container_with_border",
        css_styles="""
            {
                border: 1px solid rgba(49, 51, 63, 0.2);
                border-radius: 0.5rem;
                padding: calc(1em - 1px)
            }
            """,
    ):
            st.metric(label = 'Service Rating', value = data.loc[data['name'] == selected_restaurant, 'serviceRatingSummary'].iloc[0])
    with m3:
        with stylable_container(
        key="container_with_border",
        css_styles="""
            {
                border: 1px solid rgba(49, 51, 63, 0.2);
                border-radius: 0.5rem;
                padding: calc(1em - 1px)
            }
            """,
    ):
            st.metric(label = 'Max Party Size', value = data.loc[data['name'] == selected_restaurant, 'maxPartySize'].iloc[0])
    with m4:
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
            st.metric(label= 'Michelin?', value=data.loc[data['name'] == selected_restaurant,'michelin'].iloc[0])
    with m5:
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
            st.metric(label= 'Outdour Area?', value=data.loc[data['name'] == selected_restaurant,'outdoor_area'].iloc[0])
    # style_metric_cards(border_left_color='#FFFFFF', box_shadow=False)
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    col1, col2 = st.columns([3,3], gap = 'medium')
    with col1:
        st.image(data.loc[data['name'] == selected_restaurant, 'photo'].iloc[0])
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
            if st.button(f"Reserve Now!"):
                st.session_state.selected_restaurant = selected_restaurant
                nav_page("Reservations")
        menu = data.loc[data['name'] == selected_restaurant, 'menu_pre_proc'].iloc[0]
        # menu = menu.strip('"')  # Remove quotes from the beginning and end
        menu = menu.replace('"{', '{')
        menu = menu.replace('}"', '}')
        menu = menu.replace("::", ":")
        menu = menu.replace('""', '"')
        menu = ast.literal_eval(menu)  # Convert the string to a dictionary

        menu_items = {}

        for section, dishes in menu.items():
            for dish, details in dishes.items():
                if section not in menu_items:
                    menu_items[section] = {}
                menu_items[section][dish] = details
        
        with st.expander("Menu:"):
            
            for section, dishes in menu_items.items():
                st.markdown(f"###### {section}:")
                for dish, details in dishes.items():
                    price = details['price'] if details['price'] else "Price Unavailable"
                    description = details['description'] if details['description'] != 'null' else ""
                    
                    if description:
                        # st.markdown(f"- {dish}: {price} € ({description})") + st.caption(description)
                        st.markdown(f" - <p> {dish}: {price} € <small> ({description}) </small> </p> ", unsafe_allow_html=True)
                        
                    else:
                        st.markdown(f"- {dish}: {price} €")


    
    # select the menu_pre_proc columns for the respective selected restaurant
    

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

