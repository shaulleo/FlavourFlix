import streamlit as st
import pandas as pd
from functions.streamlitfunc import *



user_data_df = pd.DataFrame(columns=[
    "Email", "First Name", "Last Name", "Gender", "Date of Birth", "Nationality",
    "City", "Has Travel Car", "Drinks Alcohol", "Dietary Restrictions",
    "Allergies", "Favourite Food", "Dislike Food", "Personality", "Preferred Payment",
    "Restaurant Style", "Cuisine Type", "Lunch Hour", "Dinner Hour", "Normal Price Range",
    "Smoker"
])
#save as a csv file the user_data_df
user_data_df.to_csv("user_data.csv")


# email - temos que arranjar forma de se o utilizador já tiver feito login o email aparecer automaticamente
# e arranjar forma de caso o mail já exista e a pessoa fizer novamente fazer replace dos inputs
def client_data():
    
   
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    email = st.text_input("Email")
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
    normal_price_range = st.slider("Normal Price Range", min_value=0, max_value=100, value=(0, 50))
    cuisine_type = st.multiselect("Cuisine Type", ["Italian", "Asian", "American", "Mediterranean"])
    lunch_hour = st.slider("Lunch Hour", min_value=11, max_value=15,value=(11, 15))
    dinner_hour = st.slider("Dinner Hour", min_value=18, max_value=22, value=(18, 22))
    smoker = st.checkbox("Are you a smoker?")



    if st.button(label="Discover Your Personality :)"):
        global user_data_df
        new_data = pd.DataFrame({
            "Email": email,
            "First Name": [first_name],
            "Last Name": [last_name],
            "Gender": [gender],
            "Date of Birth": [date_of_birth],
            "Nationality": [nationality],
            "City": [city],
            "Has Travel Car": [has_travel_car],
            "Drinks Alcohol": [drinks_alcohol],
            "Dietary Restrictions": [dietary_restrictions],
            "Allergies": [allergies],
            "Favourite Food": [favourite_food],
            "Dislike Food": [dislike_food],
            "Personality": [personality],
            "Preferred Payment": [preferred_payment],
            "Restaurant Style": [restaurant_style],
            "Cuisine Type": [cuisine_type],
            "Lunch Hour": [lunch_hour],
            "Dinner Hour": [dinner_hour],
            "Normal Price Range": [normal_price_range],
            "Smoker": [smoker]
        })

        # Concatenate the new data with the existing user_data_df
        user_data_df = pd.concat([user_data_df, new_data], ignore_index=True)
        
        nav_page("Personality")

client_data()
