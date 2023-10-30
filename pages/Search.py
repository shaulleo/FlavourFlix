import streamlit as st
import pandas as pd
from functions.streamlitfunc import *

data = pd.read_csv('/Users/madalena.frango/Desktop/capstone/FlavourFlix/data/all_thefork_scrapes.csv')
# Add a header
st.header("Let us help you find the perfect restaurant for you!")

st.markdown('<br>', unsafe_allow_html=True)


col1, col2 = st.columns([1, 2])

def display_restaurant_table(dataframe):
    st.dataframe(dataframe[['name', 'location', 'cuisine', 'averagePrice', 'chefName']], width=5000, height=350, use_container_width=False, hide_index=True)

# Filter options for location, including 'all' option
locations = ["Select the location"] + ['All Locations'] + ['Current Location'] + data['location'].unique().tolist()

# Create a selectbox widget for the location filter
with col1:
    location_filter = st.selectbox("Select the location", locations)

# Filter restaurants based on location
if not location_filter or location_filter == 'all locations':
    filtered_df = data  # Show all restaurants
else:
    filtered_df = data[data['location'] == location_filter]

# Filter options for cuisine types, including 'all' option
types = ['Select the type of the restaurant'] + data['cuisine'].unique().tolist()

# Create a multiselect widget for the types of the restaurant
with col1:
    type_filter = st.multiselect("Select the type of the restaurant", types)

# Filter based on cuisine type
if not type_filter:
    filtered_df = data  # Show all restaurants
else:
    filtered_df = data[data['cuisine']].isin(type_filter)

# Create a slider widget for the average price
min_price = int(data['averagePrice'].min())
max_price = int(data['averagePrice'].max())
with col1:
    price_filter = st.slider("Select the average price range", min_value=min_price, max_value=max_price, value=(min_price, max_price))

# Filter based on average price range
filtered_df = filtered_df[filtered_df['averagePrice'].between(*price_filter)]

# Filter based on chef name
chefs = ["Select the Chef's Name"] + ['All Chefs'] + data['chefName'].unique().tolist()
#with col1:
    #chefs = ["Select the Chef's Name"] + ['All Chefs'] + data['chefName'].unique().tolist()
#with col1:
    #chef_filter = st.selectbox("Select the Chef's Name", chefs)

#if not chef_filter or chef_filter == 'All Chefs':
    #pass  # No chef filtering
#else:
    #filtered_df = filtered_df[filtered_df['chefName'] == chef_filter]

with col2:
    # Display the matching restaurants
    display_restaurant_table(filtered_df)