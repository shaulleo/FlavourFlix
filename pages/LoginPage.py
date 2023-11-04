import streamlit as st
import time
import pandas as pd
from functions.streamlitfunc import *
from streamlit_extras.stateful_button import button 


from functions.login import *


@st.cache_data
def read_user_data(path='data/flavourflixusers.csv', sep=';'):
    return pd.read_csv(path, sep=sep)

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


user_login = UserLogin()
user_login.generate_code()

if st.session_state.stage > 0:
    st.write(user_login.entry_code)
    if '@' in user_input:
        user_login.email = user_input
    else:
        user_login.username = user_input
    
    # Read the latest user data from the CSV file
    userdata = pd.read_csv('data/flavourflixusers.csv', sep=';')
    st.write(f'username in stage before verifying registration: {user_login.username}')

    if user_login.is_registered(userdata):
        st.write(f'username in stage after verifying registration: {user_login.username}')
        st.write(f'email in stage after verifying registration: {user_login.email}')
        st.write(f'entrycode in stage after verifying registration: {user_login.entry_code}')
        user_login.send_code(user_login.entry_code)

        user_code = st.text_input("Enter your code:", key='input_code')

        st.button('Submit Code', key='submit_entry_code', on_click=set_stage, args=(2,))
    else:
        st.error('Login failed! That email or username was not found. Please try again or create an account!.')


    if st.session_state.stage > 1:
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
