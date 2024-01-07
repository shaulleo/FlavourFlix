import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from functions.streamlitfunc import *
import json
from streamlit_extras.stylable_container import stylable_container

#General configurations
st.set_page_config(page_title='Testimonials', page_icon='ext_images/page_icon.png', layout= "wide" , initial_sidebar_state="collapsed")

#Import the data
with open('data/testimonials.json', 'r') as file:
    # Load the JSON data into a Python dictionary
    data = json.load(file)


def add_newlines(text: str, line_length: int=50):
    """ Adds new lines to a given text.
    Parameters:
        - text (str): Text to be formatted.
        - line_length (int): Number of characters per line.
    Returns:
        - lines (str): Formatted text."""
    #Tokenize the text
    words = text.split()
    #Create a list of lines
    lines = []
    current_line_length = 0

    #Per token, add it to the current line if it fits, otherwise start a new line
    for word in words:
        if current_line_length + len(word) <= line_length:
            if lines:
                lines[-1] += ' ' + word  
            else:
                lines.append(word) 
            current_line_length += len(word) + 1 
        else:
            lines.append(word)
            current_line_length = len(word)
    return '\n'.join(lines)


def show_testimonial(num: int=0):
    """ Shows a testimonial.
    Parameters:
        - num (int): Number of the testimonial to be shown.
    Returns:
        - None
    
    """
    #Select the testimonial data
    testimonial = data[num]
    #Create a container with a border to display the testimonial
    with stylable_container(
        key=f"container_with_border_{num}",
        css_styles="""
            {
                border: 0px solid rgb(15, 92, 156);
                background-color: #FFFFFF;
                padding: calc(1em - 1px);
                text-align: justify;
                width: 100%;
            }
        """,
    ):
        col1, col2 = st.columns([1, 4], gap='small')
        with col1:
            st.image(testimonial['Image'], width=95)
        with col2:
            st.subheader(testimonial['Client First Name'])
            st.caption(f" Date: {testimonial['Review Date']}")
            st.caption(f' Rating: {testimonial["Rating value (out of ten)"]} / 10')
        st.text(add_newlines(f'"{testimonial["Testimonial text"]}"'))


def show_complete_testimonials():
    """ Shows all the testimonials.
    Parameters:
        - None
    Returns:
        - None
    """

    display_header()
    #Aesthetic configurations
    st.markdown('<br>', unsafe_allow_html=True)
    st.title("Hear what our users have to say about us!")
    st.write('Have any feedback? Feel free to give your own opinion! We are always looking to improve our services. ')
    if st.button('Add a testimonial'):
        switch_page("contact us")

    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)

    st.markdown('<br>', unsafe_allow_html=True)
    #For each testimonial, show it in a column
    for i in range(0, len(data), 2):
        col1, col2 = st.columns([1, 1], gap='small')
        with col1:
            show_testimonial(i)
        if i + 1 < len(data): 
            with col2:
                show_testimonial(i + 1)
        st.markdown('<br>', unsafe_allow_html=True)
        st.divider()

#Check if the user is logged in
if ('authentication_status' in st.session_state) and (st.session_state['authentication_status'] == True) and ('username' in st.session_state) and ('email' in st.session_state):
    #Show the pages available when logged in and the testimonials
    pages_logged_in()
    show_complete_testimonials()
else:
    #Show the pages available when logged out and the testimonials
    pages_logged_off()
    show_complete_testimonials()
    
