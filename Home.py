import streamlit as st
import extra_streamlit_components as stx
# from st_pages import Page, show_pages, hide_pages
from functions.streamlitfunc import *
import time
from streamlit_extras.switch_page_button import switch_page 


# import pandas as pd


#data = pd.read_csv('data/preprocessed_data.csv')


st.set_page_config(page_title="FlavourFlix", page_icon=":movie_camera:",  layout='wide', initial_sidebar_state="collapsed")

header_image = "logo.jpeg"  
st.image(header_image, width=400)

detail_placeholder = st.empty()


if 'authentication_status' not in st.session_state or st.session_state['authentication_status'] ==False:
    #Se o estado de autenticação não existir ou for falso e não haver memória de userlogin,
    # mostra a Home page com as opções de login e signup
    if 'username' not in st.session_state and 'email' not in st.session_state:

        pages_logged_off()

        st.write("")
        st.header("Welcome to FlavourFlix!")
        st.write("FlavourFlix is a platform that recommends restaurants based on your preferences.")
        st.write("To get started, please log in or sign up.")
        st.write("")

        col1, col2, = st.columns(2)

        with col1:
            st.write("Not a member yet?")
            if st.button('Sign Up Now!', key='signup_button'):
                switch_page('sign up')
        with col2:
            st.write("Already have an account?")
            if st.button('Log In', key='login_button'):
                switch_page('log in')
    #Se o estado de autenticação não existir ou for falso mas há memória de user login, então
    #indica que há algum tipo de erro e manda de volta para a página do login para o refazer.
    else:
        st.error('Ups! Something went wrong. Please try login again.', icon='🚨')
        st.session_state['authentication_status'] = False
        with st.spinner('Redirecting you to the Login page...'):
            time.sleep(3)
        switch_page('log in')
else:

    #Se a autenticação for válida, mostra a Home page com as várias funcionalidades
    if 'username' in st.session_state and 'email' in st.session_state:

        pages_logged_in()

        st.write("")
        st.header(f"Welcome to FlavourFlix, {st.session_state['username']}!")
        st.write("FlavourFlix is a platform that recommends restaurants based on your preferences.")
        st.write("Feel free to search some restaurants or ask Filomena for suggestions!")
        st.write("")


        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("")
            if st.button('Chat with Filomena!', key='chat_button'):
                switch_page('filomena')
        with col2:
            st.write("")
            if st.button('Search for restaurants!', key='search_button'):
                switch_page('search')
        with col3:
            st.write("")
            if st.button('View your Profile!', key='profile_button'):
                switch_page('profile2')

    #Se tiver autenticado com true mas não há credenciais, então indica que há algum tipo de erro e manda de volta para o login          
    else:
        st.error('Ups! Something went wrong. Please try login again.', icon='🚨')
        st.session_state['authentication_status'] = False
        with st.spinner('Redirecting you to the Login page...'):
            time.sleep(3)
        switch_page('log in')
