import streamlit as st
import pandas as pd
from functions.streamlitfunc import *

data = pd.read_csv('/Users/madalena.frango/Desktop/capstone/FlavourFlix/data/all_thefork_scrapes.csv')

def restaurant_details():
    st.markdown(f"## {selected_restaurant}")
    col1, col2 = st.columns([3,3])
    with col1:
        st.image(data.loc[data['name'] == selected_restaurant, 'photo'].iloc[0])
    with col2:
        st.markdown(f"**Address:** {data.loc[data['name'] == selected_restaurant, 'address'].iloc[0]}")
        st.markdown(f"**Phone:** {data.loc[data['name'] == selected_restaurant, 'phone'].iloc[0]}")
        st.markdown(f"**Cuisine:** {data.loc[data['name'] == selected_restaurant, 'cuisine'].iloc[0]}")

if 'selected_restaurant' not in st.session_state:
    selected_restaurant = st.session_state.selected_restaurant = None
else:
    selected_restaurant = st.session_state.selected_restaurant

    

# If the user has not selected a restaurant yet, show a selectbox
if selected_restaurant is None:
    # Get a list of all the restaurants
    restaurants = data['name'].unique().tolist()
        # Add an option for no selection
    restaurants = [""] + restaurants
        # Create a selectbox for the user to choose a restaurant
    selected_restaurant = st.selectbox("Select Restaurant", restaurants)
        # Store the selected restaurant in session state
    st.session_state.selected_restaurant = selected_restaurant
    
else:
    # select in the select box the restaurant that was selected before
    selected_restaurant = st.selectbox("Select Restaurant", [selected_restaurant])
    restaurant_details()


