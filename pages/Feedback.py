import streamlit as st
import pandas as pd
import datetime
import time
from functions.streamlitfunc import *
from datetime import date
import csv
from streamlit_extras.switch_page_button import switch_page


st.set_page_config(page_title='Give Feedback', page_icon='ext_images/page_icon.png', layout= "wide" , initial_sidebar_state="collapsed")


def feedback_page():
    st.set_page_config(page_title='Give Feedback', page_icon='ext_images/page_icon.png', layout= "wide" , initial_sidebar_state="collapsed")
    st.title('Give Feedback')
    st.markdown('Give us your feedback about FlavourFlix')
    st.markdown('Please fill in the following details and click on submit')
    

    csv_file = 'feedbacks.csv'

    # Check if the CSV file exists and has data, if not create it with headers
    if not os.path.exists(csv_file) or os.path.getsize(csv_file) == 0:
        initial_data = {
            'Email': [],
            'Name': [],
            'Date': [],
            'Feedback': []
        }
        df = pd.DataFrame(initial_data)
        df.to_csv(csv_file, index=False)


    # AQUI TEMOS QUE IR BUSCAR OS DADOS À BASE DE DADOS QUE TEM AS PALAVRAS PASSE E OS UILIZADORES 
    email = st.session_state.email
    name = st.text_input('Name')
    feedback = st.text_area('Feedback')

    if st.button('Submit Feedback'):
        # take the current date
        today = datetime.datetime.today()  # Use datetime.datetime.today() for current date and time
        # convert the date to a string
        date_today = today.strftime("%d/%m/%Y")
        date = date_today

        data = {
            'Email': [email],
            'Name': [name],
            'Date': [date],
            'Feedback': [feedback]
        }

        # Load existing data from CSV
        df = pd.read_csv(csv_file)
        new_data = pd.DataFrame(data)
        df = pd.concat([df, new_data], ignore_index=True)

        # Save updated DataFrame to the CSV file
        df.to_csv(csv_file, index=False)

        st.success("Feedback stored successfully!")

def feedback_page_logged_off():
    st.warning("To give feedback you need to login first!")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('Already have an account? ')
        if st.button('Login'):
            switch_page('log in')
    with col2:
        st.markdown('Don\'t have an account? ')
        if st.button('Sign Up'):
            switch_page('sign up')




if ('authentication_status' in st.session_state) and (st.session_state['authentication_status'] == True) and ('username' in st.session_state) and ('email' in st.session_state):
    pages_logged_in()
    feedback_page()

else:
    pages_logged_off()
    feedback_page_logged_off()
