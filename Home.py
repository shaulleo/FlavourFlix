import streamlit as st
import extra_streamlit_components as stx
from st_pages import Page, show_pages, hide_pages
from functions.streamlitfunc import *
from streamlit_extras.switch_page_button import switch_page 


import pandas as pd


data = pd.read_csv('data/preprocessed_data.csv')


st.set_page_config(page_title="FlavourFlix", page_icon=":movie_camera:",  layout='wide', initial_sidebar_state="collapsed")
# st.sidebar.header("Sidebar Header")

header_image = "logo.jpeg"  
st.image(header_image, width=400)

detail_placeholder = st.empty()





if 'authentication_status' not in st.session_state or st.session_state['authentication_status'] ==False:
    show_pages(
    [
        Page("Home.py", "Home", "🏠"),
        Page("pages/LogIn.py", "Log In", ":books:"),
        Page("pages/SignUp.py", "Sign Up", ":books:"),
        Page("pages/Filomena.py", "Chat with Filomena", ":books:"),
        Page("pages/Profile.py", "Profile", ":books:"),
        Page("pages/Profile2.py", "Profile2", ":books:"),
        Page("pages/Search.py", "Search", ":books:"),
        Page("pages/Reservations.py", "Reservations", ":books:"),
        Page("pages/Restaurant.py", "Restaurant", ":books:"),
        Page("pages/Reservations.py", "Reservations", ":books:"),
    ])

    st.write("")
    st.header("Welcome to FlavourFlix!")
    st.write("FlavourFlix is a platform that recommends restaurants based on your preferences.")
    st.write("To get started, please log in or sign up.")
    st.write("")

    col1, col2, = st.columns(2)

    with col1:
        st.write("Not a member yet?")
        st.button("Sign Up Now!", key='signup_button', on_click= lambda: nav_page_from_home('sign up'))
    with col2:
        st.write("Already have an account?")
        st.button("Log In", key='login_button', on_click=lambda: switch_page('log in'))

else:

    show_pages(
    [
        Page("Home.py", "Home", "🏠"),
        # Page("pages/LogIn.py", "Log In", ":books:"),
        # Page("pages/SignUp.py", "Sign Up", ":books:"),
        Page("pages/Filomena.py", "Chat with Filomena", ":books:"),
        Page("pages/Profile.py", "Profile", ":books:"),
        Page("pages/Profile2.py", "Profile2", ":books:"),
        Page("pages/Search.py", "Search", ":books:"),
        Page("pages/Reservations.py", "Reservations", ":books:"),
        Page("pages/Restaurant.py", "Restaurant", ":books:"),
        Page("pages/Reservations.py", "Reservations", ":books:"),
    ])


    st.write("")
    st.header(f"Welcome to FlavourFlix, {st.session_state['username']}!")
    st.write("FlavourFlix is a platform that recommends restaurants based on your preferences.")
    st.write("Feel free to search some restaurants or ask Filomena for suggestions!")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("")
        st.write("Chat with Filomena!", key='chat_button', on_click=lambda: switch_page('Filomena'))
    with col2:
        st.write("")
        st.write("Search for restaurants!", key='search_button', on_click=lambda: switch_page('Search'))
    with col3:
        st.write("")
        st.write("View your profile!", key='profile_button', on_click=lambda: switch_page('Profile2'))

