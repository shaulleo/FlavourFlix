import streamlit as st
user_pic = st.file_uploader("Please upload your profile picture!", type=['png', 'jpg', 'jpeg'])

if user_pic is not None:
    bytes_data = user_pic.read()
    st.image(user_pic)