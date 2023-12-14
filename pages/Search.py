import streamlit as st
import pandas as pd
import numpy as np
from functions.streamlitfunc import *
from streamlit_extras.switch_page_button import switch_page
from functions.streamlitfunc import nav_page
from streamlit_extras.stylable_container import stylable_container
from functions.location import *
from functions.utils import *
from streamlit_folium import st_folium
import folium

st.set_page_config(page_title='Search', page_icon='ext_images/page_icon.png', layout= "wide" , initial_sidebar_state="collapsed")

data = pd.read_csv('data/preprocessed_data.csv')

st.header("Let us help you find the perfect restaurant for you!")

st.markdown('<br>', unsafe_allow_html=True)

if 'filters' not in st.session_state:
    st.session_state.filters = False



def select_to_view_details(data):
    filtered_df = data.copy()
    filtered_df.insert(0, "Details", False)

    # Rename columns
    renamed_columns = {
        'name': 'Restaurant Name',
        'location': 'Location',
        'cuisine': 'Cuisine',
        'averagePrice': 'Average Price'
    }
    filtered_df.rename(columns=renamed_columns, inplace=True)

    # Get dataframe row-selections from user with st.data_editor
    filtered_df = st.data_editor(
        filtered_df[['Details', 'Restaurant Name', 'Location', 'Cuisine', 'Average Price']],
        hide_index=True,
        column_config={"Details": st.column_config.CheckboxColumn(required=True)},
        disabled=data.columns,
        width=1000,
        height=390,
    )

    # Filter the dataframe using the temporary column, then drop the column
    selected_rows = filtered_df[filtered_df.Details == True]
    return selected_rows.drop('Details', axis=1)



def apply_filters(filtered_df):
    if 'filters' not in st.session_state:
        st.session_state.filters = True
    if st.session_state.filters == False:
        st.session_state.filters = True

    # Apply filters    
    if st.session_state.location and st.session_state.location != "All Locations":
        filtered_df = filtered_df[filtered_df['location'] == st.session_state.location]

    if st.session_state.cuisine and st.session_state.cuisine != 'All Cuisine Types':
        filtered_df = filtered_df[filtered_df['cuisine'] == st.session_state.cuisine]

    if st.session_state.min_price is not None:
        filtered_df = filtered_df[filtered_df['averagePrice'] >= st.session_state.min_price]

    if st.session_state.max_price is not None:
        filtered_df = filtered_df[filtered_df['averagePrice'] <= st.session_state.max_price]

    return filtered_df

def clear_filters():
    st.session_state.location = None
    st.session_state.cuisine = None
    st.session_state.min_price = None
    st.session_state.max_price = None
    st.session_state.filters = None

def show_results(data):
    selection = select_to_view_details(data)
    for index, row in selection.iterrows():
        button_key = f"view_details_button_{index}"
        
        if st.button(f"View Details for {row['Restaurant Name']}", key=button_key):
            st.session_state.selected_restaurant = row['Restaurant Name']
            switch_page("restaurant")

def show_filters_columns(data):

    st.subheader("Filters:")
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

    return  st.session_state.location, st.session_state.cuisine, st.session_state.min_price, st.session_state.max_price
    

def filters_page():
    filtered_df = data.copy()
    if 'applied' not in st.session_state:
        st.session_state.applied = False
    col1, col2 = st.columns([2, 5], gap='medium')

    if st.session_state.applied == False:
        with col1:
            location, cuisine, min_price, max_price = show_filters_columns(filtered_df)
            st.session_state.location = location
            st.session_state.cuisine = cuisine
            st.session_state.min_price = min_price
            st.session_state.max_price = max_price

        with col2:
            filtered_df = apply_filters(filtered_df)

            # Check if there are matching results
            if not filtered_df.empty:
                show_results(filtered_df)

                # Check if any location is selected before showing the map
                if st.session_state.location:
                    center_lat = filtered_df['latitude'].median()
                    center_long = filtered_df['longitude'].median()
                    m = folium.Map(location=(center_lat, center_long), zoom_start=12, tiles="cartodb positron")
                    for index, row in filtered_df.iterrows():
                        # Create a marker for each observation
                        folium.Marker(
                            location=[row['latitude'], row['longitude']],
                            popup=row['name'],  # Display the name in a popup
                        ).add_to(m)

                    # Render Folium map in Streamlit if a location is selected
                    st_data = st_folium(m, width=10000, height=400)
            else:
                st.markdown("#### OOoops! Mister Exigente! We couldn't find any restaurants matching your criteria. Please try again.")

filters_page()


    # HÁ UM PROBLEMINHA QUANDO METEMOS O MAPA, FAZ INTERFERENCIA COM OS RESULTADOS 



restaurant_details = {}



#Iterate through the data and store details in the dictionary
# for _, row in data.iterrows():
#     restaurant_details[row['name']] = {
#         'Location': row['location'],
#         'Cuisine': row['cuisine'],
#         'Average Price': row['averagePrice']
#         #'Chef Name': row['chefName'],
#         # Add other details you want to display
#     } 

# # Handle click events on the table rows



        
#         # If the user selects a restaurant from the list, set a flag in session state
#     if st.button(f"Make Reservations for {row['name']}"):
#         st.session_state.selected_restaurant = row['name']
#         st.write(f"You selected the restaurant: {row['name']}")
#         nav_page("reservations")







