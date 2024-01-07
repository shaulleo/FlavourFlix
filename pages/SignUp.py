#Source code: https://github.com/Frost-Codes/Streamlit-Authentication/blob/main/main.py

import streamlit as st
import streamlit_authenticator as stauth
from functions.loginandsignup_func import *
from functions.streamlitfunc import *
from streamlit_extras.switch_page_button import switch_page 

#General configurations
display_header()

def sign_up():
    """ 
    Shows the Sign Up page of FlavourFlix.
    Parameters:
        - None
    Returns:
        - None
    """

    # Show the pages available when logged out
    pages_logged_off()

    #Sign up form
    with st.form(key='signup', clear_on_submit=True):
        st.subheader(':black[Sign up to FlavourFlix now!]')
        #Ask for user credentials
        email = st.text_input(':blue[Email]', placeholder='Enter Your Email')
        username = st.text_input(':blue[Username]', placeholder='Enter Your Username')
        password1 = st.text_input(':blue[Password]', placeholder='Enter Your Password', type='password')
        password2 = st.text_input(':blue[Confirm Password]', placeholder='Confirm Your Password', type='password')

        btn1, btn2 = st.columns(2)

        with btn1:
            st.form_submit_button('Create your Account!')

        #Verify if the input credentials are valud such as email, usernames, passwords.
        if email:
            if validate_email(email):
                #Ensure email is not already in use
                if email not in get_user_emails():
                    if validate_username(username):
                        if username not in get_usernames():
                            if len(username) >= 2:
                                if len(password1) >= 6:
                                    if password1 == password2:

                                        # Add User to DB with a hashed password so we cannot know what it is.
                                        hashed_password = stauth.Hasher([password2]).generate()
                                        insert_user(email, username, hashed_password[0])

                                        st.balloons()
                                        switch_page('log in')

                                    else:
                                        st.warning('Passwords do not match')
                                else:
                                    st.warning('Password is too short! Must be at least 6 characters')
                            else:
                                st.warning('Username is too short... Try something else!')
                        else:
                            st.warning('Ups! That username is already taken... Try something else!')

                    else:
                        st.warning('Sorry. That username is not valid.')
                else:
                    st.warning('Ups! That email is already taken... Try something else!')
            else:
                st.warning('Sorry. That e-mail is not valid.')


    st.caption(
                    """
                    ---
                    Login Page and Sign Up Page created with ❤️ by SnakeByte.
                    
                    """
                )


#If the user is correctly logged in
if ('authentication_status' in st.session_state) and (st.session_state['authentication_status'] == True) and ('username' in st.session_state) and ('email' in st.session_state):
    #Show everything as normal and do not show sign up page
    pages_logged_in()
    switch_page('home')
else:
    #Show sign up page
    pages_logged_off()
    sign_up()


