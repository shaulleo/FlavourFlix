import streamlit as st
import pandas as pd
from functions.streamlitfunc import *

data = pd.read_csv('/Users/madalena.frango/Desktop/capstone/FlavourFlix/data/all_thefork_scrapes.csv')

def display_restaurant_detail(restaurant_data):
    st.title(restaurant_data['name'])
    st.write(restaurant_data['cuisine'])
    # Display more details, images, menu, reviews, etc.

def select_restaurant(data):
    selected_restaurant = st.selectbox("Select a restaurant", data['name'])
    
    # Get the selected restaurant's data from your dataset
    restaurant_data = data[data['name'] == selected_restaurant].iloc[0]
    
    # Display the restaurant detail in the placeholder
    display_restaurant_detail(restaurant_data)

select_restaurant(data) 