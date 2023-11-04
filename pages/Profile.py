import streamlit as st
import pandas as pd
from functions.streamlitfunc import *

# email - temos que arranjar forma de se o utilizador já tiver feito login o email aparecer automaticamente
# e arranjar forma de caso o mail já exista e a pessoa fizer novamente fazer replace dos inputs
email = st.text_input("Email")
first_name = st.text_input("First Name")
last_name = st.text_input("Last Name")
gender = st.selectbox("Gender", ["Male", "Female", "Other"])
date_of_birth = st.date_input("Date of Birth")
nationality = st.text_input("Nationality")
city = st.text_input("City")
has_travel_car = st.checkbox("Do you have a travel car?")
drinks_alcohol = st.checkbox("Do you drink alcohol?")
dietary_restrictions = st.multiselect("Dietary Restrictions", ["Vegetarian", "Vegan", "Gluten-Free", "Dairy-Free"])
allergies = st.text_area("Allergies")
favourite_food = st.text_area("Favourite Food")
dislike_food = st.text_area("Dislike Food")
personality = st.text_area("Personality")
preferred_payment = st.selectbox("Preferred Payment", ["Credit Card", "Cash", "Mobile Payment"])
restaurant_style = st.multiselect("Restaurant Style", ["Casual", "Fine Dining", "Fast Food", "Cafe"])
cuisine_type = st.multiselect("Cuisine Type", ["Italian", "Asian", "American", "Mediterranean"])
lunch_hour = st.slider("Lunch Hour", min_value=11, max_value=15,value=(11, 15))
dinner_hour = st.slider("Dinner Hour", min_value=18, max_value=22, value=(18, 22))
normal_price_range = st.slider("Normal Price Range", min_value=0, max_value=100, value=(0, 50))
smoker = st.checkbox("Are you a smoker?")



st.button(label="Discover Your Personality :)", on_click=lambda: nav_page("Personality"))
