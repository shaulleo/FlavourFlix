import streamlit as st
import pandas as pd
import os
from streamlit.components.v1 import html
from st_pages import Page, show_pages
import ast


@st.cache_data
def read_data(path: str='data/preprocessed_data.csv', sep:str=','):
    """ Read the data from a csv file.
    Parameters:
        - path (str): Path to the csv file.
        - sep (str): Separator of the csv file."""
    data = pd.read_csv(path, sep=sep)
    return data



#Show Pages available when logged in
def pages_logged_in():
    """ Shows the pages available when logged in.
    When the user is logged in, they have access to 
    a wider range of pages, such as the Home Page, 
    Filomena ChatBot, Profile, Reservations...
    """
    show_pages([
            Page("Home.py", "Home", "🏠"),
            Page("pages/Filomena.py", "Chat with Filomena", ":books:"),
            Page("pages/Profile.py", "Profile", "👤"),
            Page("pages/Search.py", "Search", "🔎"),
            Page("pages/Reservations.py", "Reservations", "🗓️"),
            Page("pages/Personality.py", "Personality", "🤔"),
            Page("pages/Restaurant.py", "Restaurant", "🍽️"),
            Page("pages/Testimonials.py", "Testimonials", "📝"),
            Page("pages/Contact.py", "Contact Us", "✍️"),
            Page("pages/Blog.py", "Blog Page", "📚"),])
    


#Show Pages available when logged out
def pages_logged_off():
    """ Shows the pages available when logged out.
    When the user is logged out, they have access to the Home page, 
    the authentication pages, Search page and the Restaurants page.
    """
    show_pages(
        [Page("Home.py", "Home", "🏠"),
         Page("pages/Search.py", "Search", "🔎"),
         Page("pages/Restaurant.py", "Restaurant", "🍽️"),
         Page("pages/LogIn.py", "Log In", "🔑"),
         Page("pages/SignUp.py", "Sign Up", "📝"),
         Page("pages/Testimonials.py", "Testimonials", "📝"),
         Page("pages/Contact.py", "Contact Us", "✍️"),
         Page("pages/Blog.py", "Blog Page", "📚"),])


#Define often used css styles
css_styles_center = """{   
                        border: 1px solid rgba(49, 51, 63, 0.2);
                        border-radius: 0.5rem;
                        padding: calc(1em - 10px);
                        text-align: center;
                        font-size: 20px;}"""

css_styles_justify = """{   
                        border: 1px solid rgba(49, 51, 63, 0.2);
                        border-radius: 0.5rem;
                        padding: calc(1em - 10px);
                        text-align: justify;
                        font-size: 20px;}"""

css_styles_res_dets = """
            {
                border: 1px solid rgba(49, 51, 63, 0.2);
                border-radius: 0.5rem;
                padding: calc(1em - 1px)
            }
            """

def show_schedule(restaurant:pd.DataFrame):
    """ Show the schedule of the restaurant.
    Parameters:
        - restaurant (pd.DataFrame): Restaurant information.
    Returns:
        - None
    """
    with st.expander("View Restaurant Schedule"):
        if restaurant['schedule'].iloc[0] == 'Not Available':
            st.markdown('Sorry! It seems that the restaurant did\nnot make their schedule available yet... :disappointed:')
        else:
            schedule = ast.literal_eval(restaurant['schedule'].iloc[0])
            for day, hours in schedule.items():
                st.markdown(f"###### {day}:")
                st.markdown(f" - {hours}")

def display_header():
    """ Displays the header of the page.
    Parameters:
        - None
    Returns:
        - None
    """
    header_image = "ext_images/logo1.jpeg"  
    c1, c2, c3 = st.columns([1, 1, 1], gap = 'small')
    with c2:
        st.image(header_image, width=400)
    st.divider()    
    st.markdown('<br>', unsafe_allow_html=True)
