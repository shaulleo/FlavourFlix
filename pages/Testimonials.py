import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from functions.streamlitfunc import *
import json
from streamlit_extras.stylable_container import stylable_container
import os
import time

st.set_page_config(page_title='Testimonials', page_icon='cozinheiro.png', layout= "wide" , initial_sidebar_state="collapsed")

with open('data/testimonials.json', 'r') as file:
    # Load the JSON data into a Python dictionary
    data = json.load(file)


def add_newlines(text, line_length=100):
    words = text.split()
    lines = []
    current_line_length = 0

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


icons = os.listdir('user_icons')[:-2]

def show_testimonial(num=0):
    testimonial = data[num]
    with stylable_container(
        key="container_with_border",
                css_styles="""
            {
                border: 1px solid rgba(49, 51, 63, 0.2);
                border-radius: 0.5rem;
                padding: calc(1em - 1px);
                text-align: justify;
                width: 100%;
            }
        """,
    ):
        col1, col2 = st.columns([1, 3], gap = 'small')
        with col1:
            st.image(f'user_icons/{icons[num]}', width=150)
        with col2:
            st.subheader(testimonial['name'])
            st.write(testimonial['date'])
            st.text(add_newlines(testimonial['testimonial']))


def show_complete_testimonials():
    header_image = "logo.jpeg"  
    st.image(header_image, width=400)
    st.title("Hear what our users have to say about us!")
    st.write('Have any feedback? Feel free to give your own opinion! We are always looking to improve our services. ')
    for i in range(len(data)-1):
        show_testimonial(i)
        st.markdown('<br>', unsafe_allow_html=True)


if ('authentication_status' in st.session_state) and (st.session_state['authentication_status'] == True) and ('username' in st.session_state) and ('email' in st.session_state):
    pages_logged_in()
    show_complete_testimonials()
else:
    pages_logged_off()
    show_complete_testimonials()
    
