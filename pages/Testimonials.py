import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from functions.streamlitfunc import *
import json
from streamlit_extras.stylable_container import stylable_container
import os
import time

st.set_page_config(page_title='Testimonials', page_icon='ext_images/page_icon.png', layout= "wide" , initial_sidebar_state="collapsed")

with open('data/testimonials.json', 'r') as file:
    # Load the JSON data into a Python dictionary
    data = json.load(file)


def add_newlines(text, line_length=50):
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
    header_image =  "ext_images/logo1.jpeg"   
    c1, c2, c3 = st.columns([1, 1, 1], gap = 'large')
    with c2:
        st.image(header_image, width=300)
    
    st.markdown('<br>', unsafe_allow_html=True)
    st.title("Hear what our users have to say about us!")
    st.write('Have any feedback? Feel free to give your own opinion! We are always looking to improve our services. ')
    if st.button('Add a testimonial'):
        pass

    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)

    st.markdown('<br>', unsafe_allow_html=True)
    for i in range(0, len(data), 2):
        col1, col2 = st.columns([1, 1], gap='small')
        with col1:
            show_testimonial(i)
        if i + 1 < len(data):  # Ensure there's a testimonial available at i+1
            with col2:
                show_testimonial(i + 1)
        st.markdown('<br>', unsafe_allow_html=True)
        st.divider()


if ('authentication_status' in st.session_state) and (st.session_state['authentication_status'] == True) and ('username' in st.session_state) and ('email' in st.session_state):
    pages_logged_in()
    show_complete_testimonials()
else:
    pages_logged_off()
    show_complete_testimonials()
    
