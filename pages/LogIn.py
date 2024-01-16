#Source code: https://github.com/Frost-Codes/Streamlit-Authentication/blob/main/main.py
import streamlit as st
import streamlit_authenticator as stauth
from functions.loginandsignup_func import *
from functions.streamlitfunc  import *
import time
from streamlit_extras.switch_page_button import switch_page 

#Set up the header section
st.set_page_config(page_title='Log In', page_icon='ext_images/page_icon.png', layout= "wide" , initial_sidebar_state="collapsed")
display_header()



def log_in():
    """ Displays the login page.
    Parameters:
        - None
    Returns:
        - None"""
    
    #Show the pages logged off while the user is not logged in
    pages_logged_off()

    #Find users in the database
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
    #Define the credentials for the authenticator and the login form
    for index in range(len(emails)):
        credentials['usernames'][usernames[index]] = {'name': emails[index], 'password': passwords[index]}
    Authenticator = stauth.Authenticate(credentials, cookie_name='flavourflix_auth', key='abcdef', cookie_expiry_days=0)
    email, authentication_status, username = Authenticator.login(':black[Login]', 'main')
    st.session_state['username'] = username
    st.session_state['email'] = email
    st.session_state['authentication_status'] = authentication_status
    info, info1 = st.columns(2)
    if username:
        #If the username exists, 
        if username in usernames:
            # If authentication is successful
            if authentication_status:
                #Log in
                with st.spinner('Logging you in...'):
                    time.sleep(2)
                    # let User see app
                st.sidebar.subheader(f'Welcome {username}!')
                Authenticator.logout('Log Out', 'sidebar')
                switch_page('home')
            #If authentication is unsuccessful
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
    st.caption(
                        """
                        ---
                        Login Page and Sign Up Page created with ❤️ by SnakeByte.
                        
                        """
                    )
    


#If the user is logged in, show the pages logged in and switch to the home page
if ('authentication_status' in st.session_state) and (st.session_state['authentication_status'] == True) and ('username' in st.session_state) and ('email' in st.session_state):
    pages_logged_in()
    switch_page('home')
#If the user is not logged in, show the pages logged off and prompt the user to log in or sign up
else:
    col1, col2,  = st.columns(2)
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


