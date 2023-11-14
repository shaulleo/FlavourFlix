import streamlit as st


def restaurant_card(title, description, image, url):
    """
    Display a restaurant card.

    Parameters:
        - title (str): The restaurant name.
        - description (str): A brief description of the restaurant.
        - image (str): The URL of the restaurant image.
        - url (str): The website or URL for more information about the restaurant.
    """
    with st.container():
        st.image(image)
        st.title(title)
        st.write(description)
        st.write(f"For more information, visit the [restaurant's website]({url}).")

def display_restaurants(restaurants):
    """
    Display a row of restaurant cards.

    Parameters:
        - restaurants (list of tuples): A list of restaurant information as tuples.
          Each tuple contains (title, description, image URL, and website URL).
    """
    col1, col2, col3 = st.columns(3)

    for i, restaurant_info in enumerate(restaurants):
        with col1 if i % 3 == 0 else col2 if i % 3 == 1 else col3:
            title, description, image, url = restaurant_info
            restaurant_card(title, description, image, url)

