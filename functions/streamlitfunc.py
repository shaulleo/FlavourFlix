import streamlit as st
import pandas as pd
import os
from streamlit.components.v1 import html
from st_pages import Page, show_pages


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
def page_shower():
    show_pages(
        [
            Page("Home.py", "Home", "🏠"),
            Page("pages/Filomena.py", "Chat with Filomena", ":books:"),
            Page("pages/Profile.py", "Profile", ":books:"),
            Page("pages/Profile2.py", "Profile2", ":books:"),
            Page("pages/Search.py", "Search", ":books:"),
            Page("pages/Reservations.py", "Reservations", ":books:"),
            Page("pages/Personality.py", "Personality", ":books:"),
            Page("pages/Restaurant.py", "Restaurant", ":books:"),])