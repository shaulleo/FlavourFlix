import streamlit as st
import streamlit_authenticator as stauth
import datetime
import re
from deta import Deta

DETA_KEY = 'a0pzxxqa8ye_JnxbPqmjR8rfF5hUGWXZrFy99VJqEkkP'

deta = Deta(DETA_KEY)

db = deta.Base('FlavourFlixAuth')


#Inserts users into our database. Has a data field to keep track when users created an account. Email is the primary key.
def insert_user(email, username, password):
    """
    Inserts Users into the DB
    :param email:
    :param username:
    :param password:
    :return User Upon successful Creation:
    """
    date_joined = str(datetime.datetime.now())

    return db.put({'key': email, 'username': username, 'password': password, 'date_joined': date_joined})

#Returns a dictionary of users. 
def fetch_users():
    """
    Fetch Users
    :return Dictionary of Users:
    """
    users = db.fetch()
    return users.items


def get_user_emails():
    """
    Fetch User Emails
    :return List of user emails:
    """
    users = db.fetch()
    emails = []
    for user in users.items:
        emails.append(user['key'])
    return emails


def get_usernames():
    """
    Fetch Usernames
    :return List of user usernames:
    """
    users = db.fetch()
    usernames = []
    for user in users.items:
        usernames.append(user['key'])
    return usernames


def validate_email(email):
    """
    Check Email Validity
    :param email:
    :return True if email is valid else False:
    """
    pattern = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$" #tesQQ12@gmail.com

    if re.match(pattern, email):
        return True
    return False


def validate_username(username):
    """
    Checks Validity of userName
    :param username:
    :return True if username is valid else False:
    """

    pattern = "^[a-zA-Z0-9]*$"
    if re.match(pattern, username):
        return True
    return False


def sign_up():
    with st.form(key='signup', clear_on_submit=True):
        st.subheader(':black[Sign up to FlavourFlix now!]')
        email = st.text_input(':blue[Email]', placeholder='Enter Your Email')
        username = st.text_input(':blue[Username]', placeholder='Enter Your Username')
        password1 = st.text_input(':blue[Password]', placeholder='Enter Your Password', type='password')
        password2 = st.text_input(':blue[Confirm Password]', placeholder='Confirm Your Password', type='password')

        if email:
            if validate_email(email):
                if email not in get_user_emails():
                    if validate_username(username):
                        if username not in get_usernames():
                            if len(username) >= 2:
                                if len(password1) >= 6:
                                    if password1 == password2:

                                        # Add User to DB with a hashed password so we cannot know what it is.
                                        hashed_password = stauth.Hasher([password2]).generate()
                                        insert_user(email, username, hashed_password[0])

                                        #Without hashing just to debug
                                        # insert_user(email, username, password2)
                                        # st.success(f'Your account was created successfully!')
                                        st.balloons()
                                    else:
                                        st.warning('Passwords do not match')
                                else:
                                    st.warning('Password is too Swort! Must be at least 6 characters')
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

        btn1, btn2 = st.columns(2)

        with btn1:
            st.form_submit_button('Create your Account!')

#sign_up()

# password2 = 'testes22'
# hashed_password = stauth.Hasher([password2]).generate()
# insert_user('testes22@gmail.com', 'testes22', hashed_password[0])