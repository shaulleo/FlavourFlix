import streamlit as st
from functions.streamlitfunc import *
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.stylable_container import stylable_container
from functions.utils import *
from functions.location import *
import json


#Set up the header section
st.set_page_config(page_title='Blog', page_icon='ext_images/page_icon.png', layout= "wide" , initial_sidebar_state="collapsed")
display_header()
# c1, c2, c3 = st.columns([1, 1, 1], gap = 'large')
# with c2:
#     st.image('ext_images/logo1.jpeg', width=450)

#Find the data
with open('data/blog_posts.json', 'r',  encoding='utf-8') as file:
    posts = json.load(file)

#Define css style
css_styles_blogs = """{   
                        border: 1px solid rgba(49, 51, 63, 0.2);
                        border-radius: 0.5rem;
                        padding: calc(1em - 10px);
                        text-align: center;
                        font-size: 20px;}"""

#Display the title
st.divider()
st.markdown("<h1 style='text-align: center; color: black; padding: 2px;'><b>The FlavourFlix Blog</b></h1>", unsafe_allow_html=True)
st.divider()

#Initialize session states for each post
for i in range(5):
    if f'read_{i}' not in st.session_state:
        st.session_state[f'read_{i}'] = False

#Define function to display the post
def display(post: dict):
    """ Displays the blog post.
    Parameters:
        - post (dict): Dictionary containing the blog post data.
    Returns:
        - None"""
    #Use the title within the expander
    with st.expander(f"{post['title']}", expanded=True):
        #Format the title to have a line break every 4 words
        title = post['title'].split()
        formatted_title = []
        for i in range(len(title)):
            word = title[i]
            if i == 4 or i == 8 or i == 12:
                word = f'{word}<br>'
            formatted_title.append(word)
        formatted_title = ' '.join(formatted_title)

        #Display the title, author and date
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


def click_read(post_num: int):
    """ Click the button to read the post and 
    update the respective session state.
    Parameters:
        - post_num (int): Post number.
    Returns:
        - None
        """
    st.session_state[f'read_{post_num}'] = True


st.write('')

#Display the post "sneak-peeks"
col1, col2, col3, col4, col5 = st.columns(5)
cols = [col1, col2, col3, col4, col5]

#For each post display the image, title, author and a snippet of the text
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

#Display the button to visit the website
st.button('Visit out Website', key='button_website')
st.divider()
for i in range(5):
    if st.session_state[f'read_{i}']:
        display(posts[i])
        st.divider()
st.caption("We would like to thank our friend Francisco for guiding the aesthetics of our blog. ")

            


