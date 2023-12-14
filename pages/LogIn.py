
#Homem milagreiro que permitiu isto: https://www.youtube.com/watch?v=8X1OidYYVQw&ab_channel=SnakeByte
#Source code: https://github.com/Frost-Codes/Streamlit-Authentication/blob/main/main.py

import streamlit as st
import streamlit_authenticator as stauth
from functions.loginandsignup_func import *
from pages.SignUp import *
from functions.streamlitfunc  import *
import time
from streamlit_extras.switch_page_button import switch_page 

#st.set_page_config(page_title='Restaurant', page_icon="ext_images/page_icon.png", layout="wide", initial_sidebar_state="collapsed")
header_image = "ext_images/logo1.jpeg"  
st.image(header_image, width=400)


def log_in():

    #client_data = pd.read_csv('data/clientDataClean.csv', sep=',')

    pages_logged_off()


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
    st.session_state['authentication_status'] = authentication_status

    info, info1 = st.columns(2)



    if username:
        if username in usernames:
            if authentication_status:
                with st.spinner('Logging you in...'):
                    time.sleep(2)
                    # let User see app
                st.sidebar.subheader(f'Welcome {username}!')
                Authenticator.logout('Log Out', 'sidebar')
                switch_page('home')

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
                    switch_page('sign up')



    st.markdown(
                        """
                        ---
                        Login Page and Sign Up Page created with ❤️ by SnakeByte.
                        
                        """
                    )
    



if ('authentication_status' in st.session_state) and (st.session_state['authentication_status'] == True) and ('username' in st.session_state) and ('email' in st.session_state):
    pages_logged_in()
    switch_page('home')
else:
    col1, col2,  = st.columns(2)
    pages_logged_off()
    with col2:
        log_in()
    with col1:
        st.write('')
        st.write('')
        st.write('')
        st.title('Welcome to FlavourFlix! :wave:')
        col11, col12 = st.columns(2)
        with col11:
            st.subheader("Don't have an account yet?")
            st.write('Sign up now to access the full features!')
            if st.button('Sign up now!', key='signup_button'):
                switch_page('sign up')
        with col12:
            st.subheader("Hungry?")
            st.write('Start searching now!')
            if st.button('Search', key='search'):
                switch_page('search')


