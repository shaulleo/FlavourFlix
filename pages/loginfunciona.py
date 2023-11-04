import streamlit as st
import time
import pandas as pd
from functions.streamlitfunc import *
from streamlit_extras.stateful_button import button 
from functions.login import *

@st.cache_data
def read_user_data(path='data/flavourflixusers.csv', sep=';'):
     return pd.read_csv(path, sep=sep)

st.button('Sign up now!', key='signup_button', on_click=lambda: nav_page("CreateAnAccount"))

st.title("Login to your account!")
user_input = st.text_input("Enter your username or email address", key='user_email_or_name')

if 'user_login' not in st.session_state:
    st.session_state.user_login = None
if 'user_code' not in st.session_state:
    st.session_state.user_code = ""

if button("Login", key='login_button'):
    if st.session_state.user_login is None:
        st.session_state.user_login = UserLogin()

    if '@' in user_input:
        st.session_state.user_login.email = user_input
    else:
        st.session_state.user_login.username = user_input

    userdata = pd.read_csv('data/flavourflixusers.csv', sep=';')
    if st.session_state.user_login.is_registered(userdata):
         if not st.session_state.user_login.entry_code:
            st.session_state.user_login.generate_code()
            st.session_state.user_login.send_code(st.session_state.user_login.entry_code)
            st.write(st.session_state.user_login.entry_code)
            user_row = userdata[(userdata['username'] == st.session_state.user_login.username ) | (userdata['email'] == st.session_state.user_login.email)]
            st.session_state.user_login.username = user_row['username'].values[0]
            st.session_state.user_login.email = user_row['email'].values[0]

    user_code = st.text_input("Enter your code:", key='input_code')

    if button('Submit Code', key='submit_entry_code'):
        with st.spinner('Logging you in...'):
            time.sleep(2)
        if st.session_state.user_login.verify_code(user_code):
            st.success('Login successful!')
            st.session_state.user_login.logged_on = True
            st.write(f'Welcome {st.session_state.user_login.username}! Please wait while we redirect you to your account page...')
            time.sleep(2)
            nav_page("Profile")
        else:
            st.error('Login failed! That code was incorrect. Please try again!')


