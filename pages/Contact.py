import streamlit as st
import pandas as pd
import datetime
import time
from functions.streamlitfunc import *
from streamlit_extras.switch_page_button import switch_page

#Set header
st.set_page_config(page_title='Customer Service', page_icon='ext_images/page_icon.png', layout= "wide" , initial_sidebar_state="collapsed")

def feedback_page():
    """ Displays the feedback page.
    Parameters:
        - None
    Returns:
        - None"""
    #Set up the header and titles
    st.title(f'Give us your Feedback, {st.session_state["username"]}!')
    st.markdown('We would love to hear what you have to say about FlavourFlix, Filomena and our services!\nIf you have any suggestion, including restaurant recommendations, new features or any complaint, feel free to disclose them here!')
    st.markdown('Please fill in the following details.')

    #Set up the path to the csv file
    csv_file = 'data/feedback.csv'

    #Set up the form
    email = st.session_state.email
    name = st.text_input('Name', key='client_name_f', placeholder='Enter your name')
    subject = st.selectbox('Subject', ['General', 'Testimonial','Restaurant Recommendation', 'New Feature', 'Complaint', 'Other'], key='subject_f', placeholder='Select a subject')
    feedback = st.text_area('Your Message', key='feedback_f', placeholder='Feel free to write your feature suggestions, restaurant recommendations or any other feedback or complaint here!')

    #Set up the submit button
    if st.button('Submit Contact'):

        #Find the current date
        today = datetime.datetime.today()  

        date_today = today.strftime("%d/%m/%Y")
        date = date_today

        data = {
            'Email': [email],
            'Name': [name],
            'Date': [date],
            'Subject': [subject],
            'Feedback': [feedback]
        }

        #Update the data with the new feedback
        df = pd.read_csv(csv_file)
        new_data = pd.DataFrame(data)
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(csv_file, index=False)

        #Show a success message
        st.success("Message sent with success!")
        st.markdown('Thank you for your message! We will take it into consideration as soon as possible! :smile:')
        time.sleep(3)
        with st.spinner('Redirecting you to the Home Page...'):
            time.sleep(3)
        switch_page('Home')



#If user is logged in
if ('authentication_status' in st.session_state) and (st.session_state['authentication_status'] == True) and ('username' in st.session_state) and ('email' in st.session_state):
    #Show the feedback page as normal
    pages_logged_in()
    feedback_page()
#If the user is not logged in
else:
    pages_logged_off()
    #Show a warning message and prompt user to log-in
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

