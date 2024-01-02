#import streamlit_authenticator as stauth
import datetime
import re
from deta import Deta
from functions.streamlitfunc import *
from functions.utils import *


deta = Deta(local_settings.DETA_KEY)
db = deta.Base('FlavourFlixAuth')

#Inserts users into a database.
def insert_user(email: str, username: str, password: str):
    """
    Inserts users into a Delta Database after creating their account.
    Parameters:
        - email (str): Email of the user.
        - username (str): Username of the user.
        - password (str): Password of the user.
    Returns:
        - None
    """
    #Find the current date and time.
    date_joined = str(datetime.datetime.now())
    #Insert the user into the database.
    return db.put({'key': email, 'username': username, 'password': password, 'date_joined': date_joined})

#Returns a dictionary of users. 
def fetch_users():
    """
    Find the users in the database.
    Parameters:
        - None
    Returns:
        - users.items (dict): Dictionary of Users.
    """
    users = db.fetch()
    return users.items


def get_user_emails():
    """
    Get the emails of the users.
    Parameters:
        - None
    Returns:
        - List of user emails.
    """
    #Fetch the users.
    users = db.fetch()
    #Create an empty list.
    emails = []
    #For each user in the database, append their email to the list.
    for user in users.items:
        emails.append(user['key'])
    return emails


def get_usernames():
    """
    Get the usernames of the users.
    Parameters:
        - None
    Returns:
        - usernames (list): List of user usernames.
    """
    users = db.fetch()
    usernames = []
    for user in users.items:
        usernames.append(user['key'])
    return usernames


def validate_email(email):
    """
    Verify if input email is valid.
    Parameters:
        - email (str): Email to be validated.
    Returns:
        - (bool): Whether the e-mail is valid or not.
    """

    #Regular expression for email validation.
    pattern = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$" 

    if re.match(pattern, email):
        return True
    return False


def validate_username(username):
    """
    Verify if input username is valid.
    Parameters:
        - username (str): Username to be validated.
    Returns:
        - (bool): Whether the username is valid or not.
    """
    #Regular expression for username validation.
    pattern = "^[a-zA-Z0-9]*$"
    if re.match(pattern, username):
        return True
    return False
