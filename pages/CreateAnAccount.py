import streamlit as st
import pandas as pd
from functions.streamlitfunc import *

# Load user data from the CSV file
@st.cache_data
def read_user_data():
    return pd.read_csv('data/flavourflixusers.csv', sep=';')

userdata = read_user_data()

# Streamlit UI
st.title("Sign up to FlavourFlix right now!")

# User input fields
email = st.text_input("Enter your email:")
username = st.text_input("Enter your username:")

if st.button("Create Account"):
    # Check if the email and username are not empty
    if email and username:
        # Check if the email is not already taken
        if email in userdata['email'].values:
            st.error("Email is already taken. Please choose another email.")
        else:
            # Check if the username is not already taken
            if username in userdata['username'].values:
                st.error("Username is already taken. Please choose another username.")
            else:
                # Add user data to the CSV file
                new_user = pd.DataFrame({'email': [email], 'username': [username]})
                userdata = userdata.append(new_user, ignore_index=True)
                userdata.to_csv('data/flavourflixusers.csv', sep=';')
                st.success("Account created successfully!")
                st.info("You can now log in with your new account.")
                st.button(label="Log in", on_click=lambda: nav_page("LoginPage"))


    else:
        st.warning("Please enter both email and username.")
