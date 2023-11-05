
#Homem milagreiro que permitiu isto: https://www.youtube.com/watch?v=8X1OidYYVQw&ab_channel=SnakeByte
#Source code: https://github.com/Frost-Codes/Streamlit-Authentication/blob/main/main.py

import streamlit as st
import streamlit_authenticator as stauth
from functions.loginandsignup_func import sign_up, fetch_users
from functions.streamlitfunc  import *
import time

#FALTA ACRESCENTAR BOTÃO LOGOUT


st.set_page_config(page_title='FlavourFlix', page_icon=':movie_camera:', layout='wide', initial_sidebar_state='collapsed')
header_image = "logo.jpeg"  
st.image(header_image, width=400)


sign_up_button = st.button('Sign up now!', key='signup_button', on_click=lambda: nav_page('SignUp'))

users = fetch_users()
emails = []
usernames = []
passwords = []

    #These are the credentials in the database
for user in users:
    emails.append(user['key'])
    usernames.append(user['username'])
    passwords.append(user['password'])

credentials = {'usernames': {}}
for index in range(len(emails)):
    credentials['usernames'][usernames[index]] = {'name': emails[index], 'password': passwords[index]}


Authenticator = stauth.Authenticate(credentials, cookie_name='flavourflix_auth', key='abcdef', cookie_expiry_days=0)

email, authentication_status, username = Authenticator.login(':black[Login]', 'main')

st.session_state['username'] = username
st.session_state['email'] = email

info, info1 = st.columns(2)


if username:
    if username in usernames:
        if authentication_status:
            with st.spinner('Logging you in...'):
                time.sleep(2)
                # let User see app
            st.sidebar.subheader(f'Welcome {username}!')
            Authenticator.logout('Log Out', 'sidebar')
            nav_page('Profile2')

        elif not authentication_status:
            with info:
                st.error('Incorrect password or username.')
        else:
            with info:
                st.warning('Please feed in your credentials.')
    else:
        with info:
            st.warning('Username does not exist, please sign up')
            if not authentication_status:
                 nav_page('SignUp')



st.markdown(
                    """
                    ---
                    Login Page and Sign Up Page created with ❤️ by SnakeByte.
                    
                    """
                )