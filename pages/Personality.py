from functions.streamlitfunc import *
import pickle

if 'submit' not in st.session_state:
    st.session_state['submit'] = False
if 'personality' not in st.session_state:
    st.session_state['personality'] = False
if 'personality_generated' not in st.session_state:
    st.session_state['personality_generated'] = False

# a pagina personality só aparece se utilizador estiver logged in
st.set_page_config( page_icon="ext_images\page_icon.png", layout="wide")

question_to_num = {"Strongly Disagree": 1, "Disagree": 2, "Neutral": 3, "Agree": 4, "Strongly Agree": 5}
questions = {"Willingness to Try Exotic Foods":"I am open to trying unfamiliar and exotic dishes.", 
             "Importance of Food Presentation":"The presentation and plating of my meal is very important.",
             "Value for Money in Meals":"I prioritize getting good value for price when choosing a meal.",
             "Preference for Gourmet Restaurants":"I prefer dining at high-end gourmet restaurants.",
             "Interest in Nutritional Content": "I pay a lot of attention to the nutritional content and health benefits of my meals.",
             "Frequency of Home-Cooked Meals": "I often opt for home-cooked meals over dining out.",
             "Desire for New Culinary Experiences": "It is important to me tro consistently explore new culinary experiences.",
             "Preference for Organic or Diet-Specific Foods": "I often incorporate organic or diet-specific foods (e.g., vegan, keto) in my meals.",
             "Enjoyment of Traditional or Familiar Foods": "I mostly enjoy eating traditional and/or familiar dishes.",
             "Willingness to Spend on High-Quality Ingredients": "I am willing to spend extra if it means getting high-quality ingredients.",
             }

def question_presentation(question, question_identifier, num):
    st.markdown(f"- ##### {question}")
    Q = st.select_slider(
        f'Select the degree of agreement with the previous statement.',
        options=["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"], value='Neutral', key=f"question_{num}")
    if Q is not "Choose an option": 
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
    submit_button = st.button("Submit")
    if submit_button:
        for i in questions.keys():
            if st.session_state[i] is None:
                st.error("Please answer all questions before submitting.")
                break
        st.session_state["submit"] = True
        generate_personality()
        

    
with open('personality_classification_model.pkl', 'rb') as f:
    model = pickle.load(f)


def personality_presentation(personality):
    # MOSTRAR PERSONALITY C IMAGEM E COISAS BONITAS
    pass
    # st.subheader("Discover your personality")
    # if "personality" in st.session_state:
    #     st.write(f"You are a {st.session_state['personality']}")
    # else:
    #     st.error("Personality type not found. Please complete the questionnaire.")
    #     if st.button("Try Again"):
    #         st.session_state['submit'] = False
    #         st.session_state['personality'] = None
    #         personality_inputs()


def generate_personality():
    model_input = [question_to_num[st.session_state[question]] for question in questions]
    personality_type = model.predict([model_input])[0] 
    st.session_state["personality"] = personality_type
    # st.write(f"Your predicted personality type is: {personality_type}")
    st.session_state['personality_generated'] = True
    return personality_type


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


if ('authentication_status' in st.session_state) and (st.session_state['authentication_status'] == True) and ('username' in st.session_state) and ('email' in st.session_state):
    pages_logged_in()
    header_image = "ext_images/logo.jpeg"
    data = pd.read_csv("data/training_answers/perturbed_total_answers.csv")
    if st.session_state['username'] in data['username'].values:
        personality_presentation()

if st.session_state['personality_generated'] is True: 
    personality_presentation()
else:  
    personality_inputs()