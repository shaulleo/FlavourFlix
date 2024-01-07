from functions.streamlitfunc import *
import pickle
import time
from streamlit_extras.switch_page_button import switch_page 
from functions.utils import *
from streamlit_extras.stylable_container import stylable_container
from functions.chat_bot import personality_based_recommendation

st.set_page_config(page_title='Profile', page_icon='ext_images/page_icon.png', layout= "wide" , initial_sidebar_state="auto")
display_header()


#Load the model
with open('personality_classification_model.pkl', 'rb') as f:
    model = pickle.load(f)

#Define the personalities and their descriptions
food_personalities = {
    "The Adventurer": {
        "description": "You're the culinary trailblazer, seeking out the uncharted territories of taste. Your palate is your compass, guiding you to vibrant markets and hidden eateries where exotic flavors await. From feasting on spicy Thai street food to sampling bizarre delicacies like fried insects in a bustling Asian market, you revel in the thrill of discovering new gastronomic adventures. Your motto? “Life’s too short for the same old menu!”",
        "image": "ext_images/personalities/the_adventurer.png"},
    "Fine Dining Connoisseur": {
        "description": "For you, a meal is a canvas, and every dish is a masterpiece. The symphony of flavors, the elegance of presentation, and the meticulous selection of ingredients are what elevate a dining experience to an art form. You appreciate the subtle dance between textures and savor the nuances in every bite. The ambiance of a Michelin-starred restaurant is your sanctuary, where each course is a meticulously crafted ode to gastronomy.",
        "image": "ext_images/personalities/fine_dining_connoisseur.png"},
    "Low Cost Foodie": {
        "description": "You're on a perpetual quest for the holy grail of affordable deliciousness! From street tacos in a bustling market to hidden gems serving up budget-friendly gourmet fare, you have an innate knack for finding the most scrumptious eats without burning a hole in your pocket. For you, the joy of dining is in the simple pleasures of taste, and the thrill of discovering an unbelievably tasty bargain brings an extra zing to every meal.",
        "image": "ext_images/personalities/low_cost_foodie.jpeg"},
    "Conscious Eater": {
        "description": "Your food choices are a testament to your commitment to wellness. Nutritional labels are your best friends, and farmer's markets are your playground. You meticulously curate your meals, seeking organic, low-calorie, or diet-specific options that not only nourish your body but also align with your values. You find delight in knowing that every bite contributes to your overall well-being.",
        "image": "ext_images/personalities/conscious_eater.png"},
    "Comfort Food Lover": {
        "description": "You find solace and joy in the warmth of familiar flavors that transport you to cherished memories and simpler times. Whether it's your grandmother's homemade apple pie or a steaming bowl of mac and cheese on a rainy day, these dishes evoke a sense of comfort and nostalgia. For you, food isn't just sustenance; it's a hug on a plate, soothing both the stomach and the soul.",
        "image": "ext_images/personalities/comfort_food_lover.png"}
}


#Define the questions and their mapping
question_to_num = {"Strongly Disagree": 1, "Disagree": 2, "Neutral": 3, "Agree": 4, "Strongly Agree": 5}
questions = {"Willingness to Try Exotic Foods":"I am open to trying unfamiliar and exotic dishes.", 
             "Importance of Food Presentation":"The presentation and plating of my meal is very important.",
             "Value for Money in Meals":"I prioritize getting good value for price when choosing a meal.",
             "Preference for Gourmet Restaurants":"I prefer dining at high-end gourmet restaurants.",
             "Interest in Nutritional Content": "I pay a lot of attention to the nutritional content and health benefits of my meals.",
             "Frequency of Eating Home-Cooked Meals": "I often opt for home-cooked meals over dining out.",
             "Desire for New Culinary Experiences": "It is important to me to consistently explore new culinary experiences.",
             "Preference for Organic or Diet-Specific Foods": "I often incorporate organic or diet-specific foods (e.g., vegan, keto) in my meals.",
             "Enjoyment of Traditional or Familiar Foods": "I mostly enjoy eating traditional and/or familiar dishes.",
             "Willingness to Spend on High-Quality Ingredients": "I am willing to spend extra if it means getting high-quality ingredients.",
             }

#Initialize session states
for i in questions.keys():
    if i not in st.session_state:
        st.session_state[i] = None
if 'submit' not in st.session_state:
    st.session_state['submit'] = None
if 'personality' not in st.session_state:
    st.session_state['personality'] = None
if 'personality_generated' not in st.session_state:
    st.session_state['personality_generated'] = None
if 'answered' not in st.session_state:
    st.session_state['answered'] = None
if 'current_location' not in st.session_state:
    st.session_state['current_location'] = None

#Show a question
def question_presentation(question: str, question_identifier: str, num: int):
    """ 
    Shows a question and saves the answer in the session state.
    Parameters:
        - question (str): string with the question to be presented
        - question_identifier (str): string with the name of the question
        - num (int): number of the question.
    Returns:
        - Q: the answer to the question.
    """
    st.markdown(f"- ##### {question}")
    Q = st.select_slider(
        f'Select the degree of agreement with the previous statement.',
        options=["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"], value='Neutral', key=f"question_{num}")
    if Q != "Choose an option": 
        st.write('**You selected:**', Q)
    else:
        st.write('**Please select an option**')
    st.session_state[question_identifier] = Q
    return Q

#Show the questions and receive the answers from the user
def personality_inputs():
    """ Shows the questions and receives the answers from the user.
    Parameters:
        - None
    Returns:
        - None
    """
    #Initialize the session states
    for i in questions.keys():
        st.session_state[i] = None
    st.subheader('To discover your food personality, please answer the degree to which you agree with the following statements:')
    st.markdown('<br>', unsafe_allow_html=True)

    #Show the questions
    for num, (question_identifier, question) in enumerate(questions.items()):
        question_presentation(question, question_identifier,  num)
        st.divider()
        
def restaurant_card(restaurant: pd.Series, title: str, number: int=None):
    """ Displays a card with the information of a restaurant.
    Parameters:
        - restaurant (pd.Series): Series with the information of the restaurant.
        - title (str): Title of the card.
        - number (int): Number of the card.
    """
    #Create the card
    with stylable_container(
         key="container_with_border",
            css_styles=css_styles_justify):
        st.markdown(f"<h5 style='text-align: left; color: black;'>{title}</h5>", unsafe_allow_html=True)
        col1, col2 = st.columns([4, 5], gap='small')
        with col1:
            #Show the restaurant image
            st.image(restaurant['photo'], width=200)
        with col2:
            #Show the restaurant information
            st.markdown(f"**{restaurant['name'].strip()}**")
            st.caption(f"*{restaurant['address'].strip()}*")
            st.caption(f"**Rating**: {restaurant['ratingValue']}/10.0")
        if st.button(f"View Details for {restaurant['name']}", key=f'restaurant{number}'):
            st.session_state.selected_restaurant = restaurant['name']
            switch_page("restaurant")
                        

def personality_presentation(observation: pd.Series = None):
    """ Displays the personality of the user after filling in the questionnaire.
    Parameters:
        - observation (pd.Series): Row with the user's answers.
    Returns:
        - None.
    """
    #Initialize the personality
    if 'personality' in st.session_state and st.session_state['personality'] is not None:
        personality = st.session_state['personality']
    else:
        personality = observation['personality'].values[0]

    #Aesthetic configurations to display the personality
    col1, col2, col3, col4 = st.columns([0.4, 0.1, 0.4, 0.1 ])
    with col1:
        image_path = food_personalities[personality]["image"]
        st.image(image_path, width=500, use_column_width=True, caption=f'{personality}')
    with col3:
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.subheader(f'Find your personality!')
        with stylable_container(
            key="container_with_border",
                    css_styles=css_styles_justify,
        ):
            st.markdown( f'You are a **{personality}**! {food_personalities[personality]["description"]}')
    #Display the back to search button
    back_to_search = st.button("Back to Search")
    if back_to_search:
        switch_page('search')

    #Display the restaurants recommended for the user        
    st.subheader('Based on your personality, we recommend the following restaurants:')
    st.write('')
    restaurants = personality_based_recommendation(personality=personality)
    for i in range(3):
        first_restaurant = restaurants.iloc[0]
        second_restaurant = restaurants.iloc[1]
        third_restaurant = restaurants.iloc[2]
        fourth_restaurant = restaurants.iloc[3]
        fift_restaurant = restaurants.iloc[4]
        
    # Display the restaurant cards
    restaurant_card(first_restaurant, 'Restaurant #1', '1')
    restaurant_card(second_restaurant, 'Restaurant #2', '2')
    restaurant_card(third_restaurant, 'Restaurant #3', '3')
    restaurant_card(fourth_restaurant, 'Restaurant #4', '4')
    restaurant_card(fift_restaurant, 'Restaurant #5', '5')
        
    

def generate_personality():
    """ Generates the personality of the user based on 
    the answers to the questionnaire by calling the model.
    Parameters:
        - None
    Returns:
        - None
        """
    #Get the answers from the user
    model_input = [question_to_num[st.session_state[question]] for question in questions]
    #Predict the personality
    personality_type = model.predict([model_input])[0] 
    #Save the personality in the session state
    st.session_state["personality"] = personality_type
    st.session_state['personality_generated'] = True
    save_results()

    
def save_results():
    """ Saves the results of the questionnaire in the database.
    Parameters:
        - None
    Returns:
        - None
        """
    #Store the answers
    answers = {}
    answers['username'] = st.session_state['username']
    for i in questions.keys():
        answers[i] = question_to_num[st.session_state[i]]
        answers['personality'] = st.session_state['personality']
    #Save them in the database
    answers = pd.DataFrame(answers, index=[0])
    og_answers = pd.read_csv("data/training_answers/perturbed_total_answers.csv")
    og_answers = pd.concat([og_answers, answers], axis=0)
    og_answers.to_csv("data/training_answers/perturbed_total_answers.csv", index=False)



def check_submission():
    """ Checks if the user clicked on the submit button.
    Parameters:
        - None.
    Returns:
        - None."""
    #Control session states for submission
    if 'submit' in st.session_state and st.session_state['submit'] == True:
        st.session_state['answered'] = True
        generate_personality()
        st.session_state['submit'] = False


def click_submit():
    """ Click the submit button and check if all questions were answered.
    Parameters:
        - None
    Returns:
        - None
    """
    #Check if all questions were answered and control session states for submission
    st.session_state['submit'] = True
    for i in questions.keys():
        if st.session_state[i] is None:
            st.error("Please answer all questions before submitting.")
            st.session_state['submit'] = False
            break
    check_submission()
    

#If the user is logged in correctly
if ('authentication_status' in st.session_state) and (st.session_state['authentication_status'] == True) and ('username' in st.session_state) and ('email' in st.session_state):
    #Show the pages normally
    pages_logged_in()
    data = pd.read_csv("data/training_answers/perturbed_total_answers.csv")
    #If the user has already answered the questionnaire, show the personality
    if st.session_state['username'] in data['username'].values and st.session_state['personality'] is None:
        personality_presentation(data[data['username'] == st.session_state['username']])
    elif st.session_state['personality'] is not None and st.session_state['answered'] == True:
        personality_presentation()
    #If the user has not answered the questionnaire, show the questions
    elif st.session_state['answered'] is None:
        personality_inputs()
        st.button("Submit", on_click=click_submit)
else:
    pages_logged_off()
    st.error('Ups! Something went wrong. Please try login again.', icon='🚨')
    st.session_state['authentication_status'] = False
    st.write('You need to be logged in to access this feature.')
    with st.spinner('Redirecting you to the Login page...'):
        time.sleep(3)
    switch_page('log in')
