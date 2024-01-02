from functions.streamlitfunc import *
import pickle
import time
from streamlit_extras.switch_page_button import switch_page 
from functions.utils import *
from streamlit_extras.stylable_container import stylable_container

st.set_page_config(page_title='Profile', page_icon='ext_images/page_icon.png', layout= "wide" , initial_sidebar_state="auto")

header_image = "ext_images/logo1.jpeg"  
c1, c2, c3 = st.columns([1, 1, 1], gap = 'small')
with c2:
    st.image(header_image, width=400)
st.divider()    
st.markdown('<br>', unsafe_allow_html=True)

with open('personality_classification_model.pkl', 'rb') as f:
    model = pickle.load(f)

food_personalities = {
    "The Adventurer": {
        "description": "You’re the culinary trailblazer, seeking out the uncharted territories of taste. Your palate is your compass, guiding you to vibrant markets and hidden eateries where exotic flavors await. From feasting on spicy Thai street food to sampling bizarre delicacies like fried insects in a bustling Asian market, you revel in the thrill of discovering new gastronomic adventures. Your motto? “Life’s too short for the same old menu!”",
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


def question_presentation(question, question_identifier, num):
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


def personality_inputs():
    for i in questions.keys():
        st.session_state[i] = None
    st.subheader('To discover your food personality, please answer the degree to which you agree with the following statements:')
    st.markdown('<br>', unsafe_allow_html=True)

    for num, (question_identifier, question) in enumerate(questions.items()):
        question_presentation(question, question_identifier,  num)
        st.divider()
        
            
def personality_presentation(observation = None):
    """ observation: row com os dados do utilizador """
    st.markdown('<br>', unsafe_allow_html=True)
    header_image = "ext_images/logo1.jpeg"  
    c1, c2, c3 = st.columns([1, 1, 1], gap = 'small')
    with c2:
        st.image(header_image, width=400)
    st.divider()    
    if 'personality' in st.session_state and st.session_state['personality'] is not None:
        personality = st.session_state['personality']
    else:
        personality = observation['personality'].values[0]

    #col1, col2 = st.columns([3,5])
    col1, col2, col3, col4 = st.columns([0.4, 0.1, 0.4, 0.1  ])
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
                    css_styles="""
                {
                    border: 0px solid rgb(36, 36, 37);
                    background-color: #FFFFFF;
                    padding: calc(1em - 1px);
                    text-align: justify;
                    width: 100%;
                }
            """,
        ):
            st.markdown( f'You are a **{personality}**! {food_personalities[personality]["description"]}')
    back_to_search = st.button("Back to Search")
    if back_to_search:
        switch_page('search')
    

def generate_personality():
    model_input = [question_to_num[st.session_state[question]] for question in questions]
    personality_type = model.predict([model_input])[0] 
    st.session_state["personality"] = personality_type
    # st.write(f"Your predicted personality type is: {personality_type}")
    st.session_state['personality_generated'] = True
    save_results()

    
def save_results():
    answers = {}
    answers['username'] = st.session_state['username']
    for i in questions.keys():
        answers[i] = question_to_num[st.session_state[i]]
        answers['personality'] = st.session_state['personality']
    answers = pd.DataFrame(answers, index=[0])
    og_answers = pd.read_csv("data/training_answers/perturbed_total_answers.csv")
    og_answers = pd.concat([og_answers, answers], axis=0)
    og_answers.to_csv("data/training_answers/perturbed_total_answers.csv", index=False)



def check_submission():
    if 'submit' in st.session_state and st.session_state['submit'] == True:
        st.session_state['answered'] = True
        generate_personality()
        st.session_state['submit'] = False


def click_submit():
    st.session_state['submit'] = True
    for i in questions.keys():
        if st.session_state[i] is None:
            st.error("Please answer all questions before submitting.")
            st.session_state['submit'] = False
            break
    check_submission()
    


if ('authentication_status' in st.session_state) and (st.session_state['authentication_status'] == True) and ('username' in st.session_state) and ('email' in st.session_state):
    pages_logged_in()
    header_image = "ext_images/logo1.jpeg"
    data = pd.read_csv("data/training_answers/perturbed_total_answers.csv")
    if st.session_state['username'] in data['username'].values and st.session_state['personality'] is None:
        personality_presentation(data[data['username'] == st.session_state['username']])
    elif st.session_state['personality'] is not None and st.session_state['answered'] == True:
        personality_presentation()
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
