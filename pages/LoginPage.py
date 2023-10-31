import streamlit as st
import time
import pandas as pd
from functions.streamlitfunc import *

from functions.login import *


@st.cache_data
def read_user_data():
    return pd.read_csv('data/flavourflixusers.csv', sep=';')

# def set_stage(stage):
#     st.session_state.stage = stage

def set_stage(stage, text_key=None):
    st.session_state.stage = stage
    if text_key is not None:
        st.session_state[text_key] = ""
        

userdata = read_user_data()


if 'stage' not in st.session_state:
    st.session_state.stage = 0


st.title("Login to your account!")
user_input = st.text_input("Enter your username or email address", key='user_email_or_name')
st.button("Login", key='login_button', on_click=set_stage, args=(1,))


if st.session_state.stage == 1:
    user_login = UserLogin()

    if '@' in user_input:
        user_login.email = user_input
    else:
        user_login.username = user_input
    
    # Read the latest user data from the CSV file
    userdata = pd.read_csv('data/flavourflixusers.csv', sep=';')

    if user_login.is_registered(userdata):
        user_login.generate_code()
        user_login.send_code(user_login.entry_code)

        user_code = st.text_input("Enter your code:", key='input_code')
        st.write(user_login.entry_code)

        st.button('Submit Code', key='submit_entry_code', on_click=set_stage, args=(2,))
    else:
        st.error('Login failed! That email or username was not found. Please try again or create an account!.')


    if st.session_state.stage == 2:
        with st.spinner('Logging you in...'):
            time.sleep(3)
            set_stage(7)
        if st.session_state.stage == 7:
            if user_code == user_login.entry_code:
                #set_stage(3)
                # if st.session_state.stage == 3:
                st.write("Code is correct.")
                user_login.logged_on = True
                st.success('Done!')
                
                nav_page("Profile")
            else:
                # set_stage(4)
                # if st.session_state.stage == 4:
                st.error("Code is incorrect. Please try again.")
                user_code = None
                set_stage(1, 'input_code')

if st.button('Sign up now!', key='signup_button'):
    nav_page("CreateAnAccount")


st.button('Reset', on_click=set_stage, args=(0,'user_email_or_name'), key='reset')
st.write("If you don't have an account, please register first.")
