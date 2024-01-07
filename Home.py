import streamlit as st
import extra_streamlit_components as stx
from functions.streamlitfunc import *
import time
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.stylable_container import stylable_container
from functions.utils import *
import folium
from streamlit_folium import st_folium
from functions.location import *

#Import data
data = pd.read_csv('data/preprocessed_restaurant_data.csv')
filtered_df = data.copy()

#General configurations
st.set_page_config(page_title="FlavourFlix", page_icon="ext_images/page_icon.png",  layout='wide', initial_sidebar_state = 'collapsed')
display_header() 


def show_kpis():
    """Shows the KPIs of the platform.
    Parameters:
        - None
    Returns:
        - None
    """
    #Distinct Restaurants
    cola, colb = st.columns(2)
    with cola:
        with stylable_container(
                key="container_with_border",
                css_styles=css_styles_justify,
            ):
                    st.metric(label = 'Distinct Restaurants', value = f'🍽️ {len(data.index)}')
        #Active Users
        with stylable_container(
                key="container_with_border",
                css_styles=css_styles_justify,
            ):
                    st.metric(label = 'Active Users', value = f'👥 1500+')
    with colb:
        #Satisfaction Rate
        with stylable_container(
                key="container_with_border",
                css_styles=css_styles_justify,
            ):
                    st.metric(label = 'Satisfaction Rate', value = f'⭐ 9.7/10')
        #Cuisine Types
        with stylable_container(
                key="container_with_border",
                css_styles=css_styles_justify,
            ):
                    st.metric(label = 'Cuisine Types', value = f'🍲 {len(data["cuisine"].unique())}')

def show_analytics(data: pd.DataFrame):
    """Shows the analytics of the platform.
    Parameters:
        - data (pd.DataFrame): Dataframe with the restaurant data.
    Returns:
        - None"""
    c1, c2, c3 = st.columns([0.25, 0.25, 0.5])
    #Show currently open restaurants
    with c1:
        data['currently_open'] = data['schedule'].apply(lambda x: check_if_open(x))
        open_restaurants = len(data[data['currently_open'] == 'Open'])
        with stylable_container(
            key="container_with_border",
            css_styles=css_styles_justify
        ):
            st.metric(label='Currently Open', value=f'🍽️ {open_restaurants}')
    #Show the average price
    with c2:
        avg_price = data['averagePrice'].mean()
        with stylable_container(
            key="container_with_border",
            css_styles=css_styles_justify
        ):
            st.metric(label='Average Price', value=f'💶 {avg_price:.0f}€')
    with c3:
        #Show the most common cuisine
        common_cuisines = data['cuisine'].value_counts().head(1).index[0]
        with stylable_container(
                key="container_with_border",
                css_styles=css_styles_justify,
            ):
            st.metric(label='Most Common Cuisine', value=f'🍲 {common_cuisines}')
           

def restaurant_card(restaurant: pd.Series, title: str, ratingcol:str='ratingValue'):
    """ Shows a card with the information of a restaurant.
    Parameters:
        - restaurant (pd.Series): Series with the information of the restaurant.
        - title (str): Title of the card.
        - ratingcol (str): Column to use for the rating.
    Returns:
        - None"""
    with stylable_container(
         key="container_with_border",
            css_styles=css_styles_justify):
        st.markdown(f"<h5 style='text-align: left; color: black;'>{title}</h5>", unsafe_allow_html=True)
        col1, col2 = st.columns([4, 5], gap='small')
        with col1:
            st.image(restaurant['photo'], width=200)
        with col2:
            #Show information about the restaurant
            st.markdown(f"**{restaurant['name'].strip()}**")
            st.caption(f"*{restaurant['address'].strip()}*")
            st.caption(f"**Rating**: {restaurant[ratingcol]}/10.0")
        #Show button to view details
        if st.button(f"View Details for {restaurant['name']}", key=f'highest_rated_{ratingcol}'):
            st.session_state.selected_restaurant = restaurant['name']
            switch_page("restaurant")

def show_top_rated(data: pd.DataFrame):
    """Shows the top rated restaurants.
    Parameters:
        - data (pd.DataFrame): Dataframe with the restaurant data.
    Returns:
        - None"""
    #Select ratings
    highest_rating = data[data['ratingValue'] == data['ratingValue'].max()].iloc[0]
    highest_food = data[data['foodRatingSummary'] == data['foodRatingSummary'].max()].iloc[0]
    highest_service = data[data['serviceRatingSummary'] == data['serviceRatingSummary'].max()].iloc[0]
    highest_ambience = data[data['ambienceRatingSummary'] == data['ambienceRatingSummary'].max()].iloc[0]
    st.markdown(f"<h3 style='text-align: center; color: black;'>Top Rated Restaurants</h3>", unsafe_allow_html=True)
    #Show the cards
    restaurant_card(highest_rating, 'Best Ratings', 'ratingValue')
    restaurant_card(highest_food, 'Highest Food Rating', 'foodRatingSummary')
    restaurant_card(highest_service, 'Best Service', 'serviceRatingSummary')
    restaurant_card(highest_ambience, 'Best Ambience', 'ambienceRatingSummary')
          

#If the user is not logged in or the login did not occur successfully, show a spcific Home page that prompts the usr to login or sign up
if 'authentication_status' not in st.session_state or st.session_state['authentication_status'] ==False:
    if 'username' not in st.session_state and 'email' not in st.session_state:
        pages_logged_off()
        st.markdown('<br>', unsafe_allow_html=True)
        col1, col2, = st.columns(2, gap='large')
        with col2:
            st.markdown('<br>', unsafe_allow_html=True)
            st.markdown('<br>', unsafe_allow_html=True)
            st.markdown('<br>', unsafe_allow_html=True)
            st.markdown('<br>', unsafe_allow_html=True)
            header_image = "ext_images/pnas.1913308116fig01.jpeg"  
            st.image(header_image)
        with col1:
            st.markdown(f"<h1 style='text-align: left; color: black;'>Welcome to FlavourFlix!</h1>", unsafe_allow_html=True)
            st.markdown('<br>', unsafe_allow_html=True)
            st.markdown("###### FlavourFlix is a platform that recommends restaurants based on your preferences.")
            st.markdown('<br>', unsafe_allow_html=True)
            show_kpis()
            st.caption("To get started, please log in or sign up.")
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

        col5, col6 = st.columns([1, 1], gap='large')
        with col5:
            st.write('')
            st.write('###### Still unsure? Check out the testimonials of our happy customers!')
            if st.button('Testimonials', key='testimonials_button'):
                switch_page('testimonials') 
        with col6:
            st.write('')
            st.write('###### Not sure yet? Feel free to contact us!')
            if st.button('Contact Us', key='contact_button'):
                switch_page('contact us')

    #If the user is logged in but the authentication did not occur successfully, then display an error message and redirect to the login page
    else:
        st.error('Ups! Something went wrong. Please try login again.', icon='🚨')
        st.session_state['authentication_status'] = False
        with st.spinner('Redirecting you to the Login page...'):
            time.sleep(3)
        switch_page('log in')
else:
    #If the login was successful, then display the Home page with the options available to the user
    if 'username' in st.session_state and 'email' in st.session_state:
        pages_logged_in()
        cola, colb, colc, cold, cole, colf = st.columns(6, gap='small')
        with cola:
            if st.button('Chat with Filomena', key='chat_button', use_container_width=True):
                switch_page('chat with filomena')
        with colb:
            if st.button('Search for restaurants', key='search_button', use_container_width=True):
                switch_page('search')
        with colc:
            if st.button('View your Profile', key='profile_button', use_container_width=True):
                switch_page('profile')
        with cold:
            if st.button('See testimonials', key='testimonials_button', use_container_width=True):
                switch_page('testimonials') 
        with cole:
            if st.button('Visit blog', key='blog_button', use_container_width=True):
                switch_page('blog page')
        with colf:
            if st.button('Contact Us', key='feedback_button', use_container_width=True):
                switch_page('contact us')
        st.divider()
        col1, col2, = st.columns((4,3))
        with col2:
            location_permission = st.toggle('Use my location', key='location_permission')
            if location_permission:
                if "current_location" not in st.session_state or not st.session_state.current_location:
                    # Get current location
                    current_location = Location()
                    current_location.getLocation()
                    st.session_state.current_location = current_location
                    st.session_state.use_current_location = True
                else:
                    current_location = st.session_state.current_location
                filtered_df = nearYou(current_location, filtered_df, top=100)
            else:
                filtered_df = data.copy()
                st.session_state.use_current_location = False
            st.write("")
            show_top_rated(filtered_df)


        with col1:
            st.markdown(f"<h1 style='text-align: left; color: black;'>Welcome to FlavourFlix, {st.session_state['username']}!</h1>", unsafe_allow_html=True)
            st.write("Find your new favourite portuguese restaurant!")
            st.write("")
            show_analytics(filtered_df)
            st.write("")
            with stylable_container(
                key="container_with_border",
                css_styles=css_styles_justify,
            ):
                # Check if any location is selected before showing the map
                if "current_location" not in st.session_state or not st.session_state.use_current_location or not st.session_state.current_location:
                    center_lat = filtered_df['latitude'].median()
                    center_long = filtered_df['longitude'].median()
                    m = folium.Map(location=(center_lat, center_long), zoom_start=6, tiles="OpenStreetMap")
                else:
                    center_lat = current_location.latitude
                    center_long = current_location.longitude
                    m = folium.Map(location=(center_lat, center_long), zoom_start=12, tiles="OpenStreetMap")
                for index, row in filtered_df.iterrows():
                    #Create a marker for each observation
                    folium.Marker(
                        location=[row['latitude'], row['longitude']],
                        popup=row['name'],).add_to(m)
                #Render Folium map in Streamlit if a location is selected
                st_folium(m, height=500, width=620, returned_objects=[])
                st.caption("""Note that the pins presented on the map are not the exact location of the restaurants,
                           but rather an estimation.""", unsafe_allow_html=True)
                  
    #If the user is logged in but the authentication did not occur successfully, then display an error message and redirect to the login page         
    else:
        st.error('Ups! Something went wrong. Please try login again.', icon='🚨')
        st.session_state['authentication_status'] = False
        with st.spinner('Redirecting you to the Login page...'):
            time.sleep(3)
        switch_page('log in')


