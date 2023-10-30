import streamlit as st
import extra_streamlit_components as stx

import pandas as pd

data = pd.read_csv('/Users/madalena.frango/Desktop/capstone/FlavourFlix/data/all_thefork_scrapes.csv')
#Tentar assim
#data = pd.read_csv('FlavourFlix/data/preprocessed_data.csv')


st.set_page_config(page_title="FlavourFlix", page_icon=":movie_camera:",  layout='wide', initial_sidebar_state="collapsed")
# st.sidebar.header("Sidebar Header")


#Aqui basta acrescentar ao repositório o logo da FlavourFlix e colocar o path
header_image = "/Users/madalena.frango/Desktop/capstone/FlavourFlix/logo.jpeg"  # Replace with the URL or path to your image
st.image(header_image, width=400)

detail_placeholder = st.empty()

