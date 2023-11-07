
#Homem milagreiro que permitiu isto: https://www.youtube.com/watch?v=8X1OidYYVQw&ab_channel=SnakeByte
#Source code: https://github.com/Frost-Codes/Streamlit-Authentication/blob/main/main.py

import streamlit as st
import streamlit_authenticator as stauth
from functions.loginandsignup_func import *
from pages.SignUp import *
from functions.streamlitfunc  import *
import time
from streamlit_extras.switch_page_button import switch_page 

client_data = pd.read_csv('data/clientDataClean.csv', sep=',')

#st.set_page_config(page_title='FlavourFlix', page_icon=':movie_camera:', layout='wide', initial_sidebar_state='collapsed')
header_image = "logo.jpeg"  
st.image(header_image, width=400)


show_pages(
        [
            Page("Home.py", "Home", "🏠"),
            Page("pages/LogIn.py", "Log In", ":books:"),
            Page("pages/SignUp.py", "Sign Up", ":books:"),
        ])

if st.button('Sign up now!', key='signup_button'):
    switch_page('sign up')

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


#Sinceramente não sei até que ponto faz sentido o utilizador ir logo para a página do Perfil, fazia mais sentido ir parar ao Home sempre!
if username:
    if username in usernames:
        if authentication_status:
            with st.spinner('Logging you in...'):
                time.sleep(2)
                # let User see app
            st.sidebar.subheader(f'Welcome {username}!')
            Authenticator.logout('Log Out', 'sidebar')
            switch_page('home')
            # #Se o utilizador já tiver dados preenchidos, ir para a home
            # if (username in client_data['username'].values) and (email in client_data['email'].values):
            #     user_data_row = client_data.loc[client_data['username'] == username]
            #     #if user_data_row.isnull().values.any() == False:
            #     switch_page('home')
            # #Caso contrário, ir para a página de preenchimento de dados
            #     # else:
            #     #     switch_page('profile2')
            # else:
            #     switch_page('home')
            
            

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
                 switch_page('signup')



st.markdown(
                    """
                    ---
                    Login Page and Sign Up Page created with ❤️ by SnakeByte.
                    
                    """
                )