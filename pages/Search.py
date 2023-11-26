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
# locations = ["All Locations"] + data['location'].unique().tolist() + ['Current Location']
# cuisine_types = ["All Cuisine Types"] + data['cuisine'].unique().tolist()
# min_price = int(data['averagePrice'].min())
# max_price = int(data['averagePrice'].max())
# chefs = data['chefName1'].unique().tolist()
# chefs.extend(data['chefName2'].unique().tolist())
# chefs.extend(data['chefName3'].unique().tolist())

# chefs = ["All Chefs"] + list(set(chefs))
# #delete the nan value from chefs
# chefs.remove(np.nan)

with col1:
    
        # Create selectbox widgets for location and cuisine type
        
        
        
        # Create a slider widget for the average price range
        
        # Filter the restaurants based on user selections
        
    if 'session_state' not in st.session_state:
        st.session_state.session_state = {
            'location': None,
            'cuisine': None
        }


    locations = ["All Locations"] + data['location'].unique().tolist() + ['Current Location']
    selected_location = st.selectbox("Select Location", locations)

    # Update session_state based on location selection
    if selected_location != "All Locations":
        st.session_state.session_state['location'] = selected_location
        filtered_by_location = data[data['location'] == selected_location]
    elif selected_location == "Current Location":
        st.session_state.session_state['location'] = selected_location
        user_location = Location()
        user_location.getLocation()
        filtered_by_location = nearYou(user_location, data)
    else:
        st.session_state.session_state['location'] = None
        filtered_by_location = data  # No location filter applied

    # Update cuisine_types based on location
    if st.session_state.session_state['location']:
        cuisine_types = ["All Cuisine Types"] + filtered_by_location['cuisine'].unique().tolist()
        
        selected_cuisine = st.selectbox("Select Cuisine Type", cuisine_types)
        
        if selected_cuisine != "All Cuisine Types":
            st.session_state.session_state['cuisine'] = selected_cuisine
            filtered_by_cuisine = filtered_by_location[filtered_by_location['cuisine'] == selected_cuisine].copy()
        else:
            st.session_state.session_state['cuisine'] = None
            filtered_by_cuisine = filtered_by_location.copy()  # No cuisine filter applied
    else:
        selected_cuisine = st.selectbox("Select Cuisine Type", ["All Cuisine Types"])
        st.session_state.session_state['cuisine'] = None
        filtered_by_cuisine = filtered_by_location.copy()  # No location filter applied





    # Display the resulting dataframe
    
    st.divider()

        # Display the matching restaurants
        
        
filtered_df = filtered_by_cuisine.copy()

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







