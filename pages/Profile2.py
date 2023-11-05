import streamlit as st
import pandas as pd
from functions.streamlitfunc import *
from datetime import date

header_image = "logo.jpeg"  
st.image(header_image, width=400)
st.title(f'Welcome to your Profile, {st.session_state["username"]}!')

#client_data = read_data('data/clientDataClean.csv', sep=',')
client_data = pd.read_csv('data/clientDataClean.csv', sep=',')

st.write('Note that you are free to not fill in any of the fields below. However, the more information you provide, the more accurate your recommendations will be.')
st.write('The collected data will be used exclusively for the purpose of providing you with the best possible recommendations.\nYour data will not be shared with any third parties.')


#Nota: temos q ver estas select boxes melhor...
def gather_client_data():

    email = st.session_state['email']
    username = st.session_state['username']


    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    date_of_birth = st.date_input("When were you born?", max_value = date.today(), format="YYYY/MM/DD")
    nationality = st.text_input("Nationality")
    city = st.text_input("Which cistrict are you based in?")


    has_travel_car = st.checkbox("Do you commonly prefer to travel by car?")
    drinks_alcohol = st.checkbox("Do you drink alcohol?")
    smoker = st.checkbox("Are you a smoker?")

    dietary_restrictions = st.selectbox("Dietary Restrictions", ["None", "Vegetarian", "Vegan"])
    allergies = st.text_input("Do you have any allergies?")

    favourite_food = st.text_area("What is your favourite food? Feel free to write in Portuguese!")
    dislike_food = st.text_area("What is your least favourite food? Feel free to write in Portuguese!")
    
    
    preferred_payment = st.selectbox("How do you prefer to pay?", ['MBWay', 'Cash', 'Credit Card', 'Apple Pay', 'Visa Electron',
       'Visa', 'Mastercard', 'Paypal', 'American Express', 'Maestro Card'])
    

    restaurant_style = st.selectbox("What Restaurant Style do you prefer?", ['Familiar', 'After Work', 'Homemade', 'Traditional',
       'Contemporary', 'Author', 'Cosy', 'Healthy', 'Central', 'Groups',
       'Bistro', 'Terrace', 'Romantic', 'Lunch', 'Organic', 'Fine Dining',
       'Nightlife', 'Street Food', 'View', 'Friendly', 'Breakfast',
       'Ceremony', 'Oceanfront', 'Wine bar', 'Business'])


    normal_price_range = st.number_input("What is the average price (in Euros) you believe is fair per meal per person?", min_value=0, max_value=100, value=15)

    cuisine_type = st.selectbox("Cuisine Type", ['Seafood', 'Portuguese', 'Mediterranean', 'Meat Cuisine', 
       'American', 'Italian', 'International', 'Pizzeria', 'European',
       'Steakhouse', 'African', 'Indian', 'Asian', 'Japanese', 'Fusion',
       'Brazilian', 'Mexican', 'Grilled', 'Vegetarian', 'Chinese',
       'Greek'])
    

    lunch_hour = st.slider("Lunch Hour", min_value=11, max_value=15,value=(11, 15))
    dinner_hour = st.slider("Dinner Hour", min_value=18, max_value=22, value=(18, 22))


    if st.button(label="Save", key="save_data"):
        user_data = {
            "email": email,
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "gender": gender,
            "date_of_birth": date_of_birth,
            "nationality": nationality,
            "city": city,
            "travel_car": has_travel_car,
            "drinks_alcohol": drinks_alcohol,
            "dietary_restrictions": dietary_restrictions.lower(),
            "allergies": allergies.lower(),
            "favourite_food": favourite_food.lower(),
            "dislike_food": dislike_food.lower(),
            "preferred_payment": preferred_payment,
            "restaurant_style": restaurant_style.lower(),
            "cuisine_type": cuisine_type.lower(),
            "lunch_hour": f'{lunch_hour[0]}:00 - {lunch_hour[1]}:00',
            "dinner_hour": f'{dinner_hour[0]}:00 - {dinner_hour[1]}:00',
            "normal_price_range": normal_price_range,
            "smoker_n": smoker
        }


        # Concatenate the new data with the existing clientdata
        client_data.append(pd.DataFrame([user_data]), ignore_index=True)

        #Export the data
        client_data.to_csv('data/clientDataClean.csv', index=False)
        


email = st.session_state['email']
username = st.session_state['username']


#Se o utilizador já tiver preenchido os dados, simplesmente extrair os q ja colocu, exibir e dar a opção de mudar
if email in list(client_data['email']) or username in list(client_data['username']):
    st.dataframe(client_data.loc[client_data['email'] == email])
#Se o utilizador não tiver preenchido os dados, dar a opção de preencher
else:
    email = st.session_state['email']
    username = st.session_state['username']
    gather_client_data()


if st.button('Discover Your Personality :)', key='personality'):
    nav_page('Personality')
        

