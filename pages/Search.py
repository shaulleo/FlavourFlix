import streamlit as st
import pandas as pd
import numpy as np
from functions.streamlitfunc import *
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.stylable_container import stylable_container
from functions.location import *
from functions.preprocessement import *
from functions.utils import *
from streamlit_folium import st_folium
import folium

st.set_page_config(page_title='Search', page_icon='ext_images/page_icon.png', layout= "wide" , initial_sidebar_state="collapsed")

data = pd.read_csv('data/preprocessed_restaurant_data.csv')
data['location'] = data['location'].apply(lambda x: standardize_location(x))
data['menu_standard'] = data['menu_pre_proc'].apply(lambda x: standardize_text(x))


#Capitalize the beginning of words in the location column
data['location'] = data['location'].apply(lambda x: x.title())

st.header("Let us help you find the perfect restaurant for you!")
st.markdown('<br>', unsafe_allow_html=True)
st.markdown('<br>', unsafe_allow_html=True)
if 'filters' not in st.session_state:
    st.session_state.filters = False
    #Significa que ainda não capturou a localização do user
if 'current_location' not in st.session_state:
    st.session_state.current_location = False
    #Por default a nao ser q o utilizador tenha expresso que quer a localização, não vai ser usada a localização atual
if 'use_current_location' not in st.session_state:
    st.session_state.use_current_location = False
if 'menu_search' not in st.session_state:
    st.session_state.menu_search = None


def apply_filters(filtered_df):
    if 'filters' not in st.session_state:
        st.session_state.filters = True
    if st.session_state.filters == False:
        st.session_state.filters = True

    if st.session_state.location and st.session_state.location != "All Locations":
        if st.session_state.location == 'Current Location':
            if st.session_state.current_location == False:
                current_location = Location()
                current_location.getLocation()
                st.session_state.current_location = current_location
            filtered_df = nearYou(st.session_state.current_location, filtered_df)

        else:
            filtered_df = filtered_df[filtered_df['location'] == st.session_state.location]

    if st.session_state.cuisine and st.session_state.cuisine != 'All Cuisine Types':
        filtered_df = filtered_df[filtered_df['cuisine'] == st.session_state.cuisine]

    if st.session_state.min_price is not None:
        filtered_df = filtered_df[filtered_df['averagePrice'] >= st.session_state.min_price]

    if st.session_state.max_price is not None:
        filtered_df = filtered_df[filtered_df['averagePrice'] <= st.session_state.max_price]
    
    if st.session_state.menu_search is not None:
        menu_search = standardize_text(st.session_state.menu_search)
        if menu_search != "":
            m1 = filtered_df['menu_en'].str.contains(menu_search, case=False, na=False)
            m2 = filtered_df['menu_pt'].str.contains(menu_search, case=False, na=False)
            m3 = filtered_df['menu_pre_proc'].str.contains(menu_search, case=False, na=False)
            filtered_df = filtered_df[m1 | m2 | m3]

    return filtered_df

def clear_filters():
    st.session_state.location = None
    st.session_state.cuisine = None
    st.session_state.min_price = None
    st.session_state.max_price = None
    st.session_state.filters = None
    st.session_state.menu_search = None


def show_filters_columns(data):
    locations = ["All Locations"] + ['Current Location'] + data['location'].unique().tolist()
    selected_location = st.selectbox("Select Location", locations, key='selected_location', index=0)
    if selected_location != "All Locations":
        st.session_state.location = selected_location
    else:
        st.session_state.location = None

    cuisine_types = ["All Cuisine Types"] + data['cuisine'].unique().tolist()
    selected_cuisine = st.selectbox("Select Cuisine Type", cuisine_types, key='selected_cuisine' )
    if selected_cuisine != "All Cuisine Types":
        st.session_state.cuisine = selected_cuisine
    else:
        st.session_state.cuisine = None

    # Price Filters
    min_price = int(data['averagePrice'].min())
    max_price = int(data['averagePrice'].max())
    price_range = st.slider("Select Price Range", min_price, max_price, (min_price, max_price), key='selected_price_range')

    # Set session state for min_price and max_price
    st.session_state.min_price = price_range[0] if price_range[0] != min_price else None
    st.session_state.max_price = price_range[1] if price_range[1] != max_price else None

    # Search by meal
    menu_search_input = st.text_input("Craving anything in specific?", value="", key='menu_search_input', placeholder="Feel free to write in Portuguese")
    if menu_search_input != "":
        st.session_state.menu_search = menu_search_input
    else:
        st.session_state.menu_search = None

    return  st.session_state.location, st.session_state.cuisine, st.session_state.min_price, st.session_state.max_price, st.session_state.menu_search

def show_results(data):
    N_cards_per_row = 3
    j = 0
    for n_row, row in data.reset_index().iterrows():
        i = n_row%N_cards_per_row
        if i==0:
            st.write("---")
            cols = st.columns(N_cards_per_row, gap="large")
        with cols[n_row%N_cards_per_row]:
            with st.container():
                st.image(row['photo'], width=250)
            st.markdown(f"**{row['name'].strip()}**")
            st.markdown(f"*{row['address'].strip()}*")
            st.markdown(f"**Cuisine Type: {row['cuisine']}**")
            button_key = f"view_details_button_{j}"
            if st.button(f"View Details for {row['name']}", key=button_key):
                st.session_state.selected_restaurant = row['name']
                switch_page("restaurant")
            j += 1

def filters_page():
    filtered_df = data.copy()
    if 'applied' not in st.session_state:
        st.session_state.applied = False
    col1, col2 = st.columns([2, 5], gap='medium')

    if st.session_state.applied == False:
        with col1:
            location, cuisine, min_price, max_price, menu_search = show_filters_columns(filtered_df)
            st.session_state.location = location
            st.session_state.cuisine = cuisine
            st.session_state.min_price = min_price
            st.session_state.max_price = max_price
            st.session_state.menu_search = menu_search

        with col2:
            filtered_df = apply_filters(filtered_df)
            # Check if there are matching results
            if not filtered_df.empty:
                show_results(filtered_df)
            else:
                st.markdown("#### Ups! We couldn't find any restaurants matching your criteria. :disappointed: Please try a different search. ")
                st.markdown('<br>', unsafe_allow_html=True)
                st.markdown('Do you have any suggestions for new restaurants? Please share them with us by clicking on the "Suggest a Restaurant" button below.')
                if st.button("Suggest a Restaurant"):
                    switch_page("contact us")


if ('authentication_status' in st.session_state) and (st.session_state['authentication_status'] == True) and ('username' in st.session_state) and ('email' in st.session_state):
    pages_logged_in()
    filters_page()

else:
    pages_logged_off()
    filters_page()


restaurant_details = {}










