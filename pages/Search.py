import streamlit as st
import pandas as pd
import numpy as np
from functions.streamlitfunc import *
from streamlit_extras.switch_page_button import switch_page
from functions.streamlitfunc import nav_page
from streamlit_extras.stylable_container import stylable_container
from functions.location import *
from streamlit_folium import st_folium
import folium

from streamlit_extras.switch_page_button import switch_page 

st.set_page_config(page_title='Search', page_icon=None, layout= "wide" , initial_sidebar_state="collapsed")

data = pd.read_csv('data/preprocessed_data.csv')

st.header("Let us help you find the perfect restaurant for you!")

st.markdown('<br>', unsafe_allow_html=True)


col1, col2 = st.columns([2, 5], gap = 'medium') 

# Filter options for location, cuisine type, and average price 
locations = ["All Locations"] + data['location'].unique().tolist() + ['Current Location']
cuisine_types = ["All Cuisine Types"] + data['cuisine'].unique().tolist()
min_price = int(data['averagePrice'].min())
max_price = int(data['averagePrice'].max())
chefs = data['chefName1'].unique().tolist()
chefs.extend(data['chefName2'].unique().tolist())
chefs.extend(data['chefName3'].unique().tolist())

chefs = ["All Chefs"] + list(set(chefs))
#delete the nan value from chefs
chefs.remove(np.nan)

with col1:
    
        # Create selectbox widgets for location and cuisine type
        location_filter = st.selectbox("Select Location", locations)
        cuisine_filter = st.selectbox("Select Cuisine Type", cuisine_types)
        chef_filter = st.selectbox("Select Chef's Name", chefs)
        # Create a slider widget for the average price range
        price_filter = st.slider("Select the Average Price Range", min_value=min_price, max_value=max_price, value=(min_price, max_price))
        # Filter the restaurants based on user selections
        
        filtered_df = data.copy()

        if location_filter != "All Locations":
            filtered_df = filtered_df[filtered_df['location'] == location_filter]
        elif location_filter == 'Current Location':
            user_location = Location()
            user_location.getLocation()
            filtered_df = nearYou(user_location, filtered_df)
        if cuisine_filter != "All Cuisine Types":
            filtered_df = filtered_df[filtered_df['cuisine'] == cuisine_filter]
        if chef_filter != "All Chefs":
            filtered_df = filtered_df[(filtered_df['chefName1'] == chef_filter) | (filtered_df['chefName2'] == chef_filter) | (filtered_df['chefName3'] == chef_filter)]
            


        filtered_df = filtered_df[filtered_df['averagePrice'].between(price_filter[0], price_filter[1])]

with col2:    
    # Display the matching restaurants 
    st.dataframe(filtered_df[['name', 'location', 'cuisine', 'averagePrice']], height=350, use_container_width=True, hide_index=True)
    #st.map(filtered_df[['latitude', 'longitude']])
    center_lat = filtered_df['latitude'].median()
    center_long = filtered_df['longitude'].median()
    m = folium.Map(location=(center_lat, center_long), zoom_start=12, tiles="cartodb positron")
    for index, row in filtered_df.iterrows():
        # Create a marker for each observation
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=row['name'],  # Display the name in a popup
        ).add_to(m)

    # call to render Folium map in Streamlit
    st_data = st_folium(m, width=725)


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

for index, row in filtered_df.iterrows():
    # col1, col2 = st.columns([1, 3], gap = 'tiny')
    if st.button(f"View Details for {row['name']}"):
        st.session_state.selected_restaurant = row['name']
        switch_page("restaurant")

        
#         # If the user selects a restaurant from the list, set a flag in session state
#     if st.button(f"Make Reservations for {row['name']}"):
#         st.session_state.selected_restaurant = row['name']
#         st.write(f"You selected the restaurant: {row['name']}")
#         nav_page("reservations")
