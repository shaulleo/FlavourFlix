import streamlit as st
import pandas as pd
# import importlib.util as ilu

# folder = 'C:\Users\carolinashaul\Documents\GitHub\FlavourFlix'
# spec = ilu.spec_from_file_location('login', folder+'/login.py')
# login = ilu.module_from_spec(spec)
# spec.loader.exec_module(login)

from functions.login import *
# Read user data from CSV file (assuming it contains 'email' and 'username' columns)
userdata = pd.read_csv('data/flavourflixusers.csv', sep=';')

st.title("Login Page")

user_login = UserLogin()

# User input fields
user_input = st.text_input("Enter your username or email address")


# Check if the user is registered
if st.button("Login"):
    if '@' in user_input:
        user_login.email = user_input
    else:
        user_login.username = user_input
    

    if user_login.is_registered(userdata):
        user_login.generate_code()
        user_login.send_code(user_login.entry_code)

        user_code = st.text_input("Enter your code:")

        # Check if the user entered the code and submitted it
        if st.button("Submit Code"):
            if user_code == user_login.entry_code:
                user_login.logged_on = True
                st.success("Login successful!")
            else:
                st.error("Code is incorrect. Please try again.")
                user_code = None  
                login_successful = False
    else:
        st.error('Login failed! That email or username was not found. Please try again.')

# Reset button
if st.button("Reset"):
    user_login.email = None
    user_login.username = None
    user_login.logged_on = False

st.write("If you don't have an account, please register first.")


