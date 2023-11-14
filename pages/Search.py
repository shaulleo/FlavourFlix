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

def select_to_view_details(data):
        df_with_selections = data.copy()
        df_with_selections.insert(0, "Details", False)

        # Get dataframe row-selections from user with st.data_editor
        edited_df = st.data_editor(
            df_with_selections[[ 'Details', 'name', 'location','cuisine', 'averagePrice']],
            hide_index=True,
            column_config={"Details": st.column_config.CheckboxColumn(required=True)},
            disabled=data.columns,
            width=1000,
            height=390
        )

        # Filter the dataframe using the temporary column, then drop the column
        selected_rows = edited_df[edited_df.Details == True]
        return selected_rows.drop('Details', axis=1)

col1, col2 = st.columns([2, 5], gap = 'medium') 

# Filter options for location, cuisine type, and average price 

#acho q nao pode ser location mas sim "city", se não fica muito esparso; inclusive tem q ser a localização standardizada para evitar questões tipo "Lisbon- Lisboa"
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
            if location_filter == 'Current Location':
                user_location = Location()
                user_location.getLocation()
                filtered_df = nearYou(user_location, filtered_df)
        if cuisine_filter != "All Cuisine Types":
            filtered_df = filtered_df[filtered_df['cuisine'] == cuisine_filter]
        if chef_filter != "All Chefs":
            filtered_df = filtered_df[(filtered_df['chefName1'] == chef_filter) | (filtered_df['chefName2'] == chef_filter) | (filtered_df['chefName3'] == chef_filter)]
            


        filtered_df = filtered_df[filtered_df['averagePrice'].between(price_filter[0], price_filter[1])]

        st.divider()

        # Display the matching restaurants
        
        

with col2:    
    selection = select_to_view_details(filtered_df)
    for index, row in selection.iterrows():
    # Use the index as a unique key for each button
            button_key = f"view_details_button_{index}"
            
            if st.button(f"View Details for {row['name']}", key=button_key):
                st.session_state.selected_restaurant = row['name']
                switch_page("restaurant")


    

    # st.dataframe(filtered_df[['name', 'location', 'cuisine', 'averagePrice']], height=350, use_container_width=True, hide_index=True)
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
    st_data = st_folium(m, width=725, height=400)


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







