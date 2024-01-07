import streamlit as st
import pandas as pd
import time
from functions.streamlitfunc import *
from datetime import date
from streamlit_extras.switch_page_button import switch_page 
from functions.utils import *
from streamlit_extras.stylable_container import stylable_container

#Initial configurations
st.set_page_config(page_title='Profile', page_icon='ext_images/page_icon.png', layout= "wide" , initial_sidebar_state="collapsed")
display_header()

#Initialize session states
if 'save' not in st.session_state:
    st.session_state['save'] = None
if 'edit' not in st.session_state:
    st.session_state['edit'] = None
if 'run' not in st.session_state:
    st.session_state['run'] = 1
if 'user_data' not in st.session_state:
    st.session_state['user_data'] = None


def click_save(user_data: dict):
    """Control session states and save user data after clicking save button.
    Parameters:
        - user_data (dict): dictionary with user data.
    Returns:
        - None"""
    st.session_state['save'] = True
    st.session_state['edit'] = False
    st.session_state['run'] += 1
    save_user_data(user_data)

def click_edit():
    """Control session states and edit user data after clicking edit button.
    Parameters:
        - None
    Returns:
        - None"""
    st.session_state['edit'] = True
    st.session_state['save'] = False
    st.session_state['run'] += 1

def gather_client_data():
    """Gather user data from the form.
    Parameters:
        - None
    Returns:
        - None"""
    
    #Find email and username
    email = st.session_state['email']
    username = st.session_state['username']
    #Set title
    st.markdown(f'## {username}, please fill in the following information for more accurate recommendations.')
    st.caption("Note that the information you provide will only be used to improve your experience on our website.\nWe will never share your personal information with third parties.")

    st.divider()
    #Personal Information Subsection
    st.markdown('### Personal Information')

    #Forms for personal information
    col1, col2 = st.columns(2)
    with col1:
        first_name = st.text_input("**First Name**", key=f'first_name_{st.session_state["run"]}')
        gender = st.selectbox("**How do you identify yourself?**",[ 'Female', 'Male', 'Other'], key=f'gender_{st.session_state["run"]}')
        nationality = st.text_input('**What is your nationality?**', key=f'nationality_{st.session_state["run"]}')
    with col2:
        last_name = st.text_input("**Last Name**", key=f'last_name_{st.session_state["run"]}')
        dob = st.date_input("**When were you born?**", min_value= date.fromisoformat('1899-12-31'), max_value = date.fromisoformat('2005-12-31'), format="YYYY/MM/DD", value=date.fromisoformat('2005-01-01'), key=f'dob_{st.session_state["run"]}')
        district = st.selectbox("**Where are you based in?**",['   ','Aveiro', 'Beja', 'Braga', 'Bragança', 'Castelo Branco', 'Coimbra', 'Évora', 'Faro', 'Guarda', 'Leiria', 'Lisboa', 'Portalegre', 'Porto', 'Santarém', 'Setúbal', 'Viana do Castelo', 'Vila Real', 'Viseu', 'Açores', 'Madeira'], key=f'district_{st.session_state["run"]}')
    
    st.divider()
    #Lifestyle and General Preferences Subsection
    st.markdown('### Lifestyle and General Preferences')

    #Forms for lifestyle and general preferences
    col3, col4 = st.columns(2)
    with col3:
        st.write('')
        has_car = st.checkbox('Do you commonly prefer to travel by car?', key=f'has_car_{st.session_state["run"]}')
        drinks_alcohol = st.checkbox('Do you drink alcohol?', key=f'drinks_alcohol_{st.session_state["run"]}')
        smoker = st.checkbox('Are you a smoker?', key=f'smoker_{st.session_state["run"]}')
    with col4:
        preferred_payment = st.selectbox("**How do you prefer to pay?**", ['   ','MBWay', 'Cash', 'Credit Card', 'Apple Pay', 'Visa Electron',
        'Visa', 'Mastercard', 'Paypal', 'American Express', 'Maestro Card'], key=f'preferred_payment_{st.session_state["run"]}')
        normal_price_range = st.number_input("**What is the average price (in Euros) you believe is fair per meal per person?**", min_value=0, max_value=100, value=15, key=f'normal_price_range_{st.session_state["run"]}')
    lunch_hour = st.slider("**Lunch Hour**", min_value=11, max_value=15,value=(11, 15), key=f'lunch_hour_{st.session_state["run"]}')
    dinner_hour = st.slider("**Dinner Hour**", min_value=18, max_value=23,value=(18, 23), key=f'dinner_hour_{st.session_state["run"]}')

    st.divider()
    #Dietary Preferences Subsection
    st.markdown('### Dietary Preferences')

    #Forms for dietary preferences
    dietary_restrictions = st.selectbox("**Dietary Restrictions**", ["None", "Vegetarian", "Vegan"], key=f'dietary_restrictions_{st.session_state["run"]}')
    allergies = st.text_input("**Do you have any allergies? If so, which?**", key=f'allergies_{st.session_state["run"]}')
    favourite_food = st.text_area("**What is your favourite food? Feel free to write in Portuguese!**", key=f'favourite_food_{st.session_state["run"]}')
    dislike_food = st.text_area("**What is your least favourite food? Feel free to write in Portuguese!**", key=f'dislike_food_{st.session_state["run"]}')
    
    st.divider()
    #Restaurant Preferences Subsection
    st.markdown('### Restaurant Preferences')

    #Forms for restaurant preferences
    restaurant_style = st.selectbox("**What Restaurant Style do you prefer?**", ['   ','Festivities', 'Chill Out', 'Buffet', 'Family', 'Modern',
       'Fine Dining', 'Groups', 'Central Location', 'Friends',
       'Not Available', 'Brunch', 'Casual', 'Homemade', 'Meetings',
       'View', 'Café', 'Breakfast', 'Street Food', 'Healthy', 'Ethnic'], key=f'restaurant_style_{st.session_state["run"]}')
    cuisine_type = st.selectbox("**Cuisine Type**", ['   ','International', 'Japanese', 'Indian', 'Portuguese', 'Italian',
       'Pizzeria', 'Mediterranean', 'Fusion', 'Nepalese', 'European',
       'Seafood', 'Vegan', 'Traditional', 'Steakhouse', 'Greek',
       'Vegetarian', 'Varied', 'Grilled', 'Thai', 'Mexican', 'Asian',
       'French', 'South American', 'Pub grub', 'Brazilian', 'Venezuelan',
       'Peruvian', 'Meat', 'Korean', 'American', 'Spanish', 'African',
       'Syrian', 'Iranian', 'Lebanese', 'Chinese', 'Tibetan',
       'Vietnamese', 'Argentinian'], key=f'cuisine_type_{st.session_state["run"]}')

    #Save user data in a dictionary
    user_data = {
            "email": email,
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "gender": gender,
            "date_of_birth": dob,
            "nationality": standardize_text(nationality),
            "city": district,
            "travel_car": has_car,
            "drinks_alcohol": drinks_alcohol,
            "dietary_restrictions": dietary_restrictions.lower(),
            "allergies": standardize_text(allergies),
            "favourite_food": standardize_text(favourite_food),
            "dislike_food": standardize_text(dislike_food),
            "preferred_payment": preferred_payment,
            "restaurant_style": restaurant_style.lower(),
            "cuisine_type": cuisine_type.lower(),
            "lunch_hour": f'{lunch_hour[0]}:00 - {lunch_hour[1]}:00',
            "dinner_hour": f'{dinner_hour[0]}:00 - {dinner_hour[1]}:00',
            "normal_price_range": normal_price_range,
            "smoker_n": smoker
        }
    
    #Update session state
    st.session_state['user_data'] = user_data


def save_user_data(user_data: dict):
    """Save user data in a csv file.
    Parameters:
        - user_data (dict): dictionary with user data.
    Returns:
        - None"""
    
    #Read client data
    client_data = pd.read_csv('data/clientData.csv', sep=',')
    #Append new data
    client_data = pd.concat([client_data, pd.DataFrame([user_data])], ignore_index=True)
    #Drop duplicates
    client_data.drop_duplicates(subset=['email', 'username'], keep = 'last', inplace=True)

    #Save data
    if not any(x =='   ' for x in user_data.values()) and not (user_data['first_name'] == '' and user_data['last_name'] == ''):
        client_data.to_csv('data/clientDataClean.csv', index=False)
        with st.spinner('Saving your data...'):
            time.sleep(3)
            st.success('Data Saved!', icon='🚀')
    else:
            st.error('Please fill in all the fields!', icon='🚨')   


def show_client_data(client_data: pd.DataFrame, email: str):
    """Show user data in a stylable container.
    Parameters:
        - client_data (pd.DataFrame): dataframe with user data.
        - email (str): user email.
    Returns:
        - None"""
    
    #CSS styles
    st.title(f'{st.session_state["username"]}\'s Profile')
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('### Personal Information 😊')
    st.markdown('<br>', unsafe_allow_html=True)

    #Display user data
    c1, c2, c3 = st.columns(3)
    with c1:
        with stylable_container(key="container_with_border", css_styles=css_styles_justify):
                st.markdown(f'**First Name:** {client_data.loc[client_data["email"] == email]["first_name"].values[0].capitalize()}')

        with stylable_container(key="container_with_border", css_styles=css_styles_justify):
                st.markdown(f'**Gender:** {client_data.loc[client_data["email"] == email]["gender"].values[0]}')
                
        with stylable_container(key="container_with_border", css_styles=css_styles_justify):
                st.markdown(f'**Nationality:** {client_data.loc[client_data["email"] == email]["nationality"].values[0].capitalize()}')

    with c2:
        with stylable_container(key="container_with_border", css_styles=css_styles_justify):
                st.markdown(f'**Last Name:** {client_data.loc[client_data["email"] == email]["last_name"].values[0].capitalize()}')
        
        with stylable_container(key="container_with_border", css_styles=css_styles_justify):
                st.markdown(f'**Birthdate:** {client_data.loc[client_data["email"] == email]["date_of_birth"].values[0]}')
        
        with stylable_container(key="container_with_border", css_styles=css_styles_justify):
                st.markdown(f'**District:** {client_data.loc[client_data["email"] == email]["city"].values[0]}')

    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('### Lifestyle and General Preferences 📱')
    st.markdown('<br>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        with stylable_container(key="container_with_border", css_styles=css_styles_justify):
                st.write(f'**Travels by Car:** {client_data.loc[client_data["email"] == email]["travel_car"].values[0]}')
                st.write(f'**Drinks Alcohol:** {client_data.loc[client_data["email"] == email]["drinks_alcohol"].values[0]}')
                st.write(f'**Smoker:** {client_data.loc[client_data["email"] == email]["smoker_n"].values[0]}')
            
    with c2:
        with stylable_container(key="container_with_border", css_styles=css_styles_justify):
                st.write(f'**Preferred Payment Method:** {client_data.loc[client_data["email"] == email]["preferred_payment"].values[0]}')
        
        with stylable_container(key="container_with_border", css_styles=css_styles_justify):
                st.write(f'**Average Price Per Meal Per Person:** {client_data.loc[client_data["email"] == email]["normal_price_range"].values[0]}')

    c1, c2 = st.columns((2,1))
    with c1:
        with stylable_container(key="container_with_border_center", css_styles=css_styles_center):
                st.write(f'**Typical Lunch Hour:** {client_data.loc[client_data["email"] == email]["lunch_hour"].values[0]}')
        with stylable_container(key="container_with_border_center", css_styles=css_styles_center):
                st.write(f'**Typical Dinner Hour:** {client_data.loc[client_data["email"] == email]["dinner_hour"].values[0]}')   
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('### Dietary Preferences 🍽️')
    st.markdown('<br>', unsafe_allow_html=True)
    c1, c2 = st.columns((2,1)) 
    with c1:
        with stylable_container(key="container_with_border", css_styles=css_styles_justify):
            st.write(f'**Dietary Restrictions:** {client_data.loc[client_data["email"] == email]["dietary_restrictions"].values[0]}')
        with stylable_container(key="container_with_border", css_styles=css_styles_justify):
            st.write(f'**Allergies:** {client_data.loc[client_data["email"] == email]["allergies"].values[0]}')
        with stylable_container(key="container_with_border", css_styles=css_styles_justify):
            st.write(f'**Favourite Food:** {client_data.loc[client_data["email"] == email]["favourite_food"].values[0]}')
        with stylable_container(key="container_with_border", css_styles=css_styles_justify):
            st.write(f'**Dislike Food:** {client_data.loc[client_data["email"] == email]["dislike_food"].values[0]}')

    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('### Restaurant Preferences 👩🏻‍🍳')
    st.markdown('<br>', unsafe_allow_html=True)
    c1, c2 = st.columns((2,1)) 
    with c1:
        with stylable_container(key="container_with_border", css_styles=css_styles_justify):
            st.write(f'Preferred Restaurant Style: {client_data.loc[client_data["email"] == email]["restaurant_style"].values[0]}')
        with stylable_container(key="container_with_border", css_styles=css_styles_justify): 
            st.write(f'Preferred Cuisine Type: {client_data.loc[client_data["email"] == email]["cuisine_type"].values[0]}')


        
    st.caption('If you would like to change any of the information above, please feel free to edit.')
    
#If logged in
if ('authentication_status' in st.session_state) and (st.session_state['authentication_status'] == True) and ('username' in st.session_state) and ('email' in st.session_state):
    pages_logged_in()
    header_image = "ext_images/logo1.jpeg"
    #Se o cliente já tiver os dados guardados
    client_data = pd.read_csv('data/clientData.csv', sep=',')
    if st.session_state['username'] in client_data['username'].values and st.session_state['email'] in client_data['email'].values:
        #E não procura editar OU visita a pagina pela primeira vez apos ter os dados guardados
        if st.session_state['edit'] == False or st.session_state['edit'] is None:
            show_client_data(client_data[client_data['username'] == st.session_state['username']], st.session_state['email'])
            st.button('Edit', on_click=click_edit, key=f'edit_{st.session_state["run"]}')
        elif st.session_state['edit'] == True:
            gather_client_data()
            st.button('Save', on_click=click_save, args=[st.session_state['user_data']], key=f'save_{st.session_state["run"]}')
    #Se o cliente não tiver os seus dados dados guardados
    else:
        st.session_state['edit'] = True
        gather_client_data()
        st.button('Save', on_click=click_save, args=[st.session_state['user_data']], key=f'save_{st.session_state["run"]}')
else:
    pages_logged_off()
    st.error('Ups! Something went wrong. Please try login again.', icon='🚨')
    st.session_state['authentication_status'] = False
    st.write('You need to be logged in to access this feature.')
    with st.spinner('Redirecting you to the Login page...'):
        time.sleep(3)
    switch_page('log in')
