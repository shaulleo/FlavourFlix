import streamlit as st
import extra_streamlit_components as stx
from functions.streamlitfunc import *
import time
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.stylable_container import stylable_container


data = pd.read_csv('data/preprocessed_data.csv')

st.set_page_config(page_title="FlavourFlix", page_icon="ext_images/page_icon.png",  layout='wide', initial_sidebar_state="collapsed")

header_image = "ext_images/logo1.jpeg"  
c1, c2, c3 = st.columns([1, 1, 1], gap = 'small')
with c2:
    st.image(header_image, width=400)
st.divider()    



def show_kpis():
    cola, colb = st.columns(2)
    with cola:
        with stylable_container(
                key="container_with_border",
                css_styles="""
                    {
                        border: 1px solid rgba(49, 51, 63, 0.2);
                        border-radius: 0.5rem;
                        padding: calc(1em - 1px);
                        text-align: justify;
                    }
                    """,
            ):
                    st.metric(label = 'Distinct Restaurants', value = f'🍽️ {len(data.index)}')
    
        with stylable_container(
                key="container_with_border",
                css_styles="""
                    {
                        border: 1px solid rgba(49, 51, 63, 0.2);
                        border-radius: 0.5rem;
                        padding: calc(1em - 1px);
                        text-align: justify;
                    }
                    """,
            ):
                    #Depois colocar aqui o número de users
                    st.metric(label = 'Active Users', value = f'👥 1500+')
    with colb:
        with stylable_container(
                key="container_with_border",
                css_styles="""
                    {
                        border: 1px solid rgba(49, 51, 63, 0.2);
                        border-radius: 0.5rem;
                        padding: calc(1em - 1px);
                        text-align: justify;
                    }
                    """,
            ):
                    st.metric(label = 'Satisfaction Rate', value = f'⭐ 9.7/10')
    
        with stylable_container(
                key="container_with_border",
                css_styles="""
                    {
                        border: 1px solid rgba(49, 51, 63, 0.2);
                        border-radius: 0.5rem;
                        padding: calc(1em - 1px);
                        text-align: justify;
                    }
                    """,
            ):
                    st.metric(label = 'Cuisine Types', value = f'🍲 {len(data["cuisine"].unique())}')



if 'authentication_status' not in st.session_state or st.session_state['authentication_status'] ==False:


    #Se o estado de autenticação não existir ou for falso e não haver memória de userlogin,
    # mostra a Home page com as opções de login e signup
    if 'username' not in st.session_state and 'email' not in st.session_state:
        pages_logged_off()
        st.markdown('<br>', unsafe_allow_html=True)
        col1, col2, = st.columns(2, gap='large')
        with col2:
            st.markdown('<br>', unsafe_allow_html=True)
            st.markdown('<br>', unsafe_allow_html=True)
            st.markdown('<br>', unsafe_allow_html=True)
            st.markdown('<br>', unsafe_allow_html=True)
            st.markdown('<br>', unsafe_allow_html=True)
            header_image = "ext_images/pnas.1913308116fig01.jpeg"  
            st.image(header_image)
            st.markdown('<br>', unsafe_allow_html=True)
            

            
    
        with col1:
    
            st.markdown(f"<h1 style='text-align: left; color: black;'>Welcome to FlavourFlix!</h1>", unsafe_allow_html=True)
            # st.header("Welcome to FlavourFlix!")
            st.markdown('<br>', unsafe_allow_html=True)
            st.markdown("###### FlavourFlix is a platform that recommends restaurants based on your preferences.")
            st.markdown('<br>', unsafe_allow_html=True)
            show_kpis()
            st.caption("To get started, please log in or sign up.")
        st.write("")
        st.divider()
        col3, col4 = st.columns([1,1], gap='large')
        with col3:
            st.write("")
            st.markdown("###### Not a member yet?")
            if st.button('Sign Up Now!', key='signup_button'):
                switch_page('sign up')
            st.write('')
            st.markdown("###### Super hungry? Start searching now!")
            if st.button('Search now!', key='search_button'):
                switch_page('search')
        with col4:
            st.write("")
            st.markdown('###### Already have an account?')
            if st.button('Log In', key='login_button'):
                switch_page('log in')
            st.write('')
            st.markdown("###### Wanna learn more? Check out our blog!")
            if st.button('Blog', key='blog_button'):
                switch_page('blog page')

        col5, col6 = st.columns([0.8, 0.2], gap='small')
        with col5:
            st.write('')
            st.write('Still unsure? Check out the\ntestimonials of our happy customers!')
        with col6:
            st.write('')
            if st.button('Testimonials', key='testimonials_button'):
                switch_page('testimonials') 
            
            
            
            
    #Se o estado de autenticação não existir ou for falso mas há memória de user login, então
    #indica que há algum tipo de erro e manda de volta para a página do login para o refazer.
    
    else:
        st.error('Ups! Something went wrong. Please try login again.', icon='🚨')
        st.session_state['authentication_status'] = False
        with st.spinner('Redirecting you to the Login page...'):
            time.sleep(3)
        switch_page('log in')


else:
    #Se a autenticação for válida, mostra a Home page com as várias funcionalidades
    if 'username' in st.session_state and 'email' in st.session_state:

        pages_logged_in()

        col1, col2, = st.columns(2)
        with col1:
            show_kpis()
            st.image("ext_images/LucilleFrankfurt-4e47171b0b684277aaea4368ecb4cc15.png")
        with col2:
            # st.write("")
            # st.header(f"Welcome to FlavourFlix, {st.session_state['username']}!")
            st.markdown(f"<h1 style='text-align: left; color: black;'>Welcome to FlavourFlix, {st.session_state['username']}!</h1>", unsafe_allow_html=True)
            st.write("FlavourFlix is a platform that recommends restaurants based on your preferences.")
            st.write("Feel free to search some restaurants or ask Filomena for suggestions!")
            st.write("")
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
                if st.button('Chat with Filomena!', key='chat_button', use_container_width=True):
                    switch_page('chat with filomena')
                if st.button('Search for restaurants!', key='search_button', use_container_width=True):
                    switch_page('search')
                if st.button('View your Profile!', key='profile_button', use_container_width=True):
                    switch_page('profile')
                if st.button('See testimonials', key='testimonials_button', use_container_width=True):
                    switch_page('testimonials')
                if st.button('Visit blog', key='blog_button', use_container_width=True):
                    switch_page('blog page')
                if st.button('Give feedback', key='feedback_button', use_container_width=True):
                    switch_page('feedback')
                  
                       
             


        # col1, col2, col3 = st.columns(3)
        # with col1:
        #     st.write("")
        #     if st.button('Chat with Filomena!', key='chat_button'):
        #         switch_page('chat with filomena')
        # with col2:
        #     st.write("")
        #     if st.button('Search for restaurants!', key='search_button'):
        #         switch_page('search')
        # with col3:
        #     st.write("")
        #     if st.button('View your Profile!', key='profile_button'):
        #         switch_page('profile')

    #Se tiver autenticado com true mas não há credenciais, então indica que há algum tipo de erro e manda de volta para o login          
    else:
        st.error('Ups! Something went wrong. Please try login again.', icon='🚨')
        st.session_state['authentication_status'] = False
        with st.spinner('Redirecting you to the Login page...'):
            time.sleep(3)
        switch_page('log in')
