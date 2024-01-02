import streamlit as st
import extra_streamlit_components as stx
from functions.streamlitfunc import *
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.stylable_container import stylable_container
from functions.utils import *
from streamlit_folium import st_folium
from functions.location import *
import json


st.set_page_config(page_title='Blog', page_icon='ext_images/page_icon.png', layout= "wide" , initial_sidebar_state="collapsed")
c1, c2, c3 = st.columns([1, 1, 1], gap = 'large')
with c2:
    st.image('ext_images/logo1.jpeg', width=450)


with open('data/blog_posts.json', 'r',  encoding='utf-8') as file:
    posts = json.load(file)


css_styles_blogs = """{   
                        border: 1px solid rgba(49, 51, 63, 0.2);
                        border-radius: 0.5rem;
                        padding: calc(1em - 10px);
                        text-align: center;
                        font-size: 20px;}"""

st.divider()
st.markdown("<h1 style='text-align: center; color: black; padding: 2px;'><b>The FlavourFlix Blog</b></h1>", unsafe_allow_html=True)

st.divider()

for i in range(5):
    if f'read_{i}' not in st.session_state:
        st.session_state[f'read_{i}'] = False

def display(post):
    with st.expander(f"{post['title']}", expanded=True):
        title = post['title'].split()
        formatted_title = []
        for i in range(len(title)):
            word = title[i]
            if i == 4 or i == 8 or i == 12:
                word = f'{word}<br>'
            formatted_title.append(word)
        formatted_title = ' '.join(formatted_title)

        st.write('')
        st.markdown(f"<h1 style='text-align: center; color: black; padding: 5px;'><b>{formatted_title}</b></h1>", unsafe_allow_html=True)
        st.markdown(f"<h7 style='text-align: left; padding: 0.5px 1px 0.5px 800px; color: black;'><i>by {post['author']}</i></h7>", unsafe_allow_html=True)
        st.write('')
        st.write('')
        st.markdown(f"<h7 style='text-align: left; padding: 0.5px 1px 0.5px 75px; color: black;'><b>{post['date']}</b></h7>", unsafe_allow_html=True)
        st.write('')
        st.write('')
        #Sections that will be in italic
        italic_sections = ['closingNote', 'finalBlogPost', 'invitation', 'upcoming']

        # Display greeting
        if 'greeting' in post['corpus'].keys():
            st.markdown(f"<p style='text-align: justify;  font-size: 110%; line-height: 1.2; padding: 1.5px 200px 1.5px 200px; color: black;'><i>{post['corpus']['greeting']}</i></p>", unsafe_allow_html=True)

        # Display the image
        cola, colb, colc = st.columns([0.3, .5, .2])
        with colb:
            st.image(post['image'], width=500)
        st.write('')

        # Display the body of text
        for section, content in post['corpus'].items():
            if section not in italic_sections:
                if isinstance(content, dict):
                    for subsection in content.keys():
                        if subsection != 'title':
                            text = content[subsection]
                            st.markdown(f"<p style='text-align: justify; font-size: 110%;  line-height: 1.2; padding: 1.5px 200px 1.5px 200px; color: black;'>{text}</p>", unsafe_allow_html=True)
                        else:
                            title = content['title']
                            st.markdown(f"<h4 style='text-align: center; padding: 1.5px 200 3px 200; color: black;'><b>{title}</b></h4>", unsafe_allow_html=True)
                            st.write('')
            else:
                st.markdown(f"<p style='text-align: justify;  font-size: 110%; line-height: 1.2; padding: 1.5px 200px 1.5px 200px; color: black;'><i>{content}</i></p>", unsafe_allow_html=True)


def click_read(post_num):
    st.session_state[f'read_{post_num}'] = True

st.write('')
col1, col2, col3, col4, col5 = st.columns(5)
cols = [col1, col2, col3, col4, col5]

for i, (col, post) in enumerate(zip(cols, posts)):
    with col:
        with stylable_container(key='container', css_styles=css_styles_blogs):
            st.image(post['image'], width=215)
            st.markdown(f"<h5 style='text-align: left; padding: 1.5px 50px 3px 2px; color: black;'><b>{post['title']}</b></h5>", unsafe_allow_html=True)
            st.write('')
            st.markdown(f"<h8 style='text-align: left; padding: 0.5px 1px 0.5px 75px; color: black;'><i>{post['author']}</i></h8>", unsafe_allow_html=True)
            text = post['full_text'].split()
            text = text[50:100]
            text = ' '.join(text)
            st.markdown(f"<p style='text-align: justify; color: grey; font-size: 70%; line-height: 1.2; padding: 1.5px 25px 3px 2px;'> ...{text}... </p>", unsafe_allow_html=True)
            st.write('')
            st.button('Continue Reading', key=f'button_{post["title"]}', on_click=click_read, args=[i])

st.button('Visit out Website', key='button_website')
st.divider()
for i in range(5):
    if st.session_state[f'read_{i}']:
        display(posts[i])
        st.divider()

            


