import streamlit as st
import pandas as pd

data = pd.read_csv('/Users/madalena.frango/Desktop/capstone/FlavourFlix/data/all_thefork_scrapes.csv')
#Tentar assim
#data = pd.read_csv('FlavourFlix/data/preprocessed_restaurant_data.csv')


st.set_page_config(page_title="FlavourFlix", page_icon=":movie_camera:",  layout='wide')

#Aqui basta acrescentar ao repositório o logo da FlavourFlix e colocar o path
header_image = "https://purepng.com/public/uploads/large/purepng.com-disney-logologobrand-logoiconslogos-251519939495wtv86.png"  # Replace with the URL or path to your image
st.image(header_image, width=100)

# Add a header
st.header("Welcome to FlavourFlix!")


types = data["cuisine"].unique()
# Create a checkbox for the "Select all" option
all_types = st.checkbox("Select all restaurants")

# Create a multiselect widget for the types of the restaurant
if all_types:
    # If the checkbox is checked, select all the types by default
    type_filter = st.multiselect("Select the type of the restaurant", types, default=types)
else:
    # If the checkbox is not checked, select none by default
    type_filter = st.multiselect("Select the type of the restaurant", types)



# Create a slider widget for the average price
min_price = int(data["averagePrice"].min())
max_price = int(data["averagePrice"].max())
price_filter = st.slider("Select the average price range", min_value=min_price, max_value=max_price, value=(min_price, max_price))

filtered_df = data[(data["cuisine"].isin(type_filter)) & (data["averagePrice"].between(*price_filter))]

# Display the matching restaurants
st.table(filtered_df[['name', 'address']])