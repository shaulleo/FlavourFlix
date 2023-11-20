import streamlit as st
import pandas as pd
import os
from streamlit.components.v1 import html
from st_pages import Page, show_pages
import ast


def nav_page(page_name, timeout_secs=3):
    nav_script = """
        <script type="text/javascript">
            function attempt_nav_page(page_name, start_time, timeout_secs) {
                var links = window.parent.document.getElementsByTagName("a");
                for (var i = 0; i < links.length; i++) {
                    if (links[i].href.toLowerCase().endsWith("/" + page_name.toLowerCase())) {
                        links[i].click();
                        return;
                    }
                }
                var elasped = new Date() - start_time;
                if (elasped < timeout_secs * 1000) {
                    setTimeout(attempt_nav_page, 100, page_name, start_time, timeout_secs);
                } else {
                    alert("Unable to navigate to page '" + page_name + "' after " + timeout_secs + " second(s).");
                }
            }
            window.addEventListener("load", function() {
                attempt_nav_page("%s", new Date(), %d);
            });
        </script>
    """ % (page_name, timeout_secs)
    html(nav_script)


@st.cache_data
def read_data(path='data/preprocessed_data.csv', sep=';'):
    data = pd.read_csv(path, sep=sep)
    return data



#Show Pages available when logged in
def pages_logged_in():
    """ Shows the pages available when logged in.
    When the user is logged in, they have access to the Home page, Search page, Profile page,
    Search page, Restaurant page, Personality page, Reservations page and ChatBot Filomena."""
    show_pages(
        [
            Page("Home.py", "Home", "🏠"),
            Page("pages/Filomena.py", "Chat with Filomena", ":books:"),
            Page("pages/Profile.py", "Profile", "👤"),
            Page("pages/Search.py", "Search", "🔎"),
            Page("pages/Reservations.py", "Reservations", "🗓️"),
            Page("pages/Personality.py", "Personality", "🤔"),
            Page("pages/Restaurant.py", "Restaurant", "🍽️"),
            Page("pages/Testimonials.py", "Testimonials", "📝"),
            Page("pages/Blog.py", "Blog Page", "📚"),])
    


#Show Pages available when logged out
def pages_logged_off():
    """ Shows the pages available when logged out.
    When the user is logged out, they have access to the Home page, the authentication pages,
    Search page and the Restaurants page.
    """
    show_pages(
        [Page("Home.py", "Home", "🏠"),
         Page("pages/Search.py", "Search", "🔎"),
         Page("pages/Restaurant.py", "Restaurant", "🍽️"),
         Page("pages/LogIn.py", "Log In", "🔑"),
         Page("pages/SignUp.py", "Sign Up", "📝"),
         Page("pages/Testimonials.py", "Testimonials", "📝"),
         Page("pages/Blog.py", "Blog Page", "📚"),])

def show_menu(selected_restaurant):               
    menu = data.loc[data['name'] == selected_restaurant, 'menu_pre_proc'].iloc[0]
    # menu = menu.strip('"')  # Remove quotes from the beginning and end
    menu = menu.replace('"{', '{')
    menu = menu.replace('}"', '}')
    menu = menu.replace("::", ":")
    menu = menu.replace('""', '"')
    menu = ast.literal_eval(menu)  # Convert the string to a dictionary

    menu_items = {}

    for section, dishes in menu.items():
        for dish, details in dishes.items():
            if section not in menu_items:
                menu_items[section] = {}
            menu_items[section][dish] = details
    
    with st.expander("Menu:"):
        
        for section, dishes in menu_items.items():
            st.markdown(f"###### {section}:")
            for dish, details in dishes.items():
                price = details['price'] if details['price'] else "Price Unavailable"
                description = details['description'] if details['description'] != 'null' else ""
                
                if description:
                    # st.markdown(f"- {dish}: {price} € ({description})") + st.caption(description)
                    st.markdown(f" - <p> {dish}: {price} € <small> ({description}) </small> </p> ", unsafe_allow_html=True)
                    
                else:
                    st.markdown(f"- {dish}: {price} €")


