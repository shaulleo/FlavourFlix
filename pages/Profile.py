import streamlit as st
import pandas as pd
import time
from functions.streamlitfunc import *
from datetime import date
from streamlit_extras.switch_page_button import switch_page 
from functions.utils import *



# ---- Este é oq quero ajuda do prof ----
def save_state(variable):
    st.session_state[f'{variable}'] = variable



def gather_client_data():
    st.session_state['edit'] = False

    email = st.session_state['email']
    username = st.session_state['username']

    # user_pic = st.file_uploader("Please upload your profile picture!", type=['png', 'jpg', 'jpeg'])
    # save_state(user_pic)

    first_name = st.text_input("First Name")
    save_state(first_name)
    last_name = st.text_input("Last Name")
    save_state(last_name)

    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    save_state(gender)

    date_of_birth = st.date_input("When were you born?", min_value= date.fromisoformat('1899-12-31'), max_value = date.today(), format="YYYY/MM/DD")
    save_state(date_of_birth)

    nationality = st.text_input("What is your Nationality?")
    save_state(nationality)

    #Falta colocar o resto
    city = st.selectbox("Which district are you based in?", ['Lisboa', 'Porto', 'Faro', 'Évora', 'Setúbal', 'Aveiro', 'Braga', 
                                                             'Coimbra', 'Leiria', 'Santarém', 'Viseu', 'Viana do Castelo',])
    save_state(city)

    has_travel_car = st.checkbox("Do you commonly prefer to travel by car?")
    save_state(has_travel_car)
    drinks_alcohol = st.checkbox("Do you drink alcohol?")
    save_state(drinks_alcohol)
    smoker = st.checkbox("Are you a smoker?")
    save_state(smoker)

    dietary_restrictions = st.selectbox("Dietary Restrictions", ["None", "Vegetarian", "Vegan"])
    save_state(dietary_restrictions)
    allergies = st.text_input("Do you have any allergies?")
    save_state(allergies)

    favourite_food = st.text_area("What is your favourite food? Feel free to write in Portuguese!")
    save_state(favourite_food)
    dislike_food = st.text_area("What is your least favourite food? Feel free to write in Portuguese!")
    save_state(dislike_food)
    
    preferred_payment = st.selectbox("How do you prefer to pay?", ['MBWay', 'Cash', 'Credit Card', 'Apple Pay', 'Visa Electron',
       'Visa', 'Mastercard', 'Paypal', 'American Express', 'Maestro Card'])
    save_state(preferred_payment)
    
    restaurant_style = st.selectbox("What Restaurant Style do you prefer?", ['Familiar', 'After Work', 'Homemade', 'Traditional',
       'Contemporary', 'Author', 'Cosy', 'Healthy', 'Central', 'Groups',
       'Bistro', 'Terrace', 'Romantic', 'Lunch', 'Organic', 'Fine Dining',
       'Nightlife', 'Street Food', 'View', 'Friendly', 'Breakfast',
       'Ceremony', 'Oceanfront', 'Wine bar', 'Business'])
    save_state(restaurant_style)

    normal_price_range = st.number_input("What is the average price (in Euros) you believe is fair per meal per person?", min_value=0, max_value=100, value=15)
    save_state(normal_price_range)

    cuisine_type = st.selectbox("Cuisine Type", ['Seafood', 'Portuguese', 'Mediterranean', 'Meat Cuisine', 
       'American', 'Italian', 'International', 'Pizzeria', 'European',
       'Steakhouse', 'African', 'Indian', 'Asian', 'Japanese', 'Fusion',
       'Brazilian', 'Mexican', 'Grilled', 'Vegetarian', 'Chinese',
       'Greek'])
    save_state(cuisine_type)
    
    lunch_hour = st.slider("Lunch Hour", min_value=11, max_value=15,value=(11, 15))
    save_state(lunch_hour)
    dinner_hour = st.slider("Dinner Hour", min_value=18, max_value=22, value=(18, 22))
    save_state(dinner_hour)

    user_data = {
            "email": email,
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "gender": gender,
            "date_of_birth": date_of_birth,
            "nationality": standardize_text(nationality),
            "city": city,
            "travel_car": has_travel_car,
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

    if st.button(label="Save", key="save_data"):
        st.session_state['save'] = True
        save_user_data(user_data)


def save_user_data(user_data: dict):
    client_data = pd.read_csv('data/clientDataCleantestes.csv', sep=',')
    # Concatenate the new data with the existing clientdata
    client_data = pd.concat([client_data, pd.DataFrame([user_data])], ignore_index=True)
    client_data.drop_duplicates(subset=['email', 'username'], keep = 'last', inplace=True)

        #Export the data
    client_data.to_csv('data/clientDataCleantestes.csv', index=False)
    with st.spinner('Saving your data...'):
        time.sleep(3)
        st.success('Data Saved!', icon='🚀')
        st.session_state['save'] = False
    show_client_data()


def show_client_data():
    email = st.session_state['email']
    username = st.session_state['username']
    
    st.session_state['save'] = False
    st.session_state['edit'] = False

    client_data = pd.read_csv('data/clientDataCleantestes.csv', sep=',')
    col1, col2 = st.columns(2)
    with col1:
        st.write(f'First Name: {client_data.loc[client_data["email"] == email]["first_name"].values[0]}')
        st.write(f'Last Name: {client_data.loc[client_data["email"] == email]["last_name"].values[0]}')
        st.write(f'Birthdate: {client_data.loc[client_data["email"] == email]["date_of_birth"].values[0]}')

        # if 'user_pic' in st.session_state:
        #     st.write('Your Profile Picture:')
        #     st.image(st.session_state['user_pic'])

        #st.write(f'Gender: {[client_data.loc["email"] == email]["gender"].values[0]}')
        st.write(f'Nationality : {client_data.loc[client_data["email"] == email]["nationality"].values[0]}')
        st.write(f'District: {client_data.loc[client_data["email"] == email]["city"].values[0]}')
        st.write(f'Smoker: {client_data.loc[client_data["email"] == email]["smoker_n"].values[0]}')
        st.write(f'Drinks Alcohol: {client_data.loc[client_data["email"] == email]["drinks_alcohol"].values[0]}')
        st.write(f'Travels by Car: {client_data.loc[client_data["email"] == email]["travel_car"].values[0]}')
    with col2:
        st.write(f'Favourite Food: {client_data.loc[client_data["email"] == email]["favourite_food"].values[0]}')
        st.write(f'Dislike Food: {client_data.loc[client_data["email"] == email]["dislike_food"].values[0]}')
        st.write(f'Dietary Restrictions: {client_data.loc[client_data["email"] == email]["dietary_restrictions"].values[0]}')
        st.write(f'Allergies: {client_data.loc[client_data["email"] == email]["allergies"].values[0]}')
        st.write(f'Preferred Payment Method: {client_data.loc[client_data["email"] == email]["preferred_payment"].values[0]}')
        st.write(f'Average Price Per Meal Per Person: {client_data.loc[client_data["email"] == email]["normal_price_range"].values[0]}')
        st.write(f'Preferred Restaurant Style: {client_data.loc[client_data["email"] == email]["restaurant_style"].values[0]}')
        st.write(f'Preferred Cuisine Type: {client_data.loc[client_data["email"] == email]["cuisine_type"].values[0]}')
        st.write(f'Typical Lunch Hour: {client_data.loc[client_data["email"] == email]["lunch_hour"].values[0]}')
        st.write(f'Typical Dinner Hour: {client_data.loc[client_data["email"] == email]["dinner_hour"].values[0]}')
    
    st.write('If you would like to change any of the information above, please feel free to edit.')
    if st.button('Edit', key='edit_button'):
        st.session_state['edit'] = True


if ('authentication_status' in st.session_state) and (st.session_state['authentication_status'] == True) and ('username' in st.session_state) and ('email' in st.session_state):
    pages_logged_in()
    header_image = "ext_images/logo.jpeg"  
    st.image(header_image, width=400)
    st.title(f'Welcome to your Profile, {st.session_state["username"]}!')
    ph = st.empty()

    if 'edit' not in st.session_state or st.session_state['edit'] == False:
        show_client_data()
    else:
        gather_client_data()
        if st.session_state['save'] == True:
            save_user_data()


else:
    pages_logged_off()
    st.error('Ups! Something went wrong. Please try login again.', icon='🚨')
    st.session_state['authentication_status'] = False
    st.write('You need to be logged in to access this feature.')
    with st.spinner('Redirecting you to the Login page...'):
        time.sleep(3)
    switch_page('log in')

if st.button('Discover Your Personality! 😀', key='personality'):
    switch_page('personality')