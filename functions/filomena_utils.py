import streamlit as st
from functions.utils import *
from sklearn.metrics.pairwise import cosine_similarity 
import spacy
import re
# !python -m spacy download en_core_web_md



#------------------------ Functions ------------------------#


def get_identification_and_user():
    if ('authentication_status' in st.session_state) and (st.session_state['authentication_status'] == True) and ('username' in st.session_state):
        username = st.session_state['username']
        client_data = pd.read_csv('data/clientData.csv')
        if username in client_data['username'].values:
            first_name = client_data[client_data['username'] == username]['first_name'].values[0]
        else:
            first_name = 'Not Provided'
        return f'User Identification:\n Username: {username} | User First Name: {first_name}'
    else:
        return f'No Identification Provided'
    

def get_profile():
    if ('authentication_status' in st.session_state) and (st.session_state['authentication_status'] == True) and ('username' in st.session_state):
        client_data = pd.read_csv('data/clientData.csv')
        personality_questionnaire = pd.read_csv('data/training_answers/perturbed_total_answers.csv')
        if st.session_state['username'] in client_data['username'].values:
            user_info = client_data[client_data['username'] == st.session_state['username']]
            user_info_formatted = f"""The information about the user is:
            - First Name: {user_info['first_name'].values[0]}
            - Gender: {user_info['gender'].values[0]}
            - Nationality: {user_info['nationality'].values[0]}
            - City: {user_info['city'].values[0]}
            - Prefers to travel by car: {user_info['travel_car'].values[0]}
            - Drinks alcohol: {user_info['drinks_alcohol'].values[0]}
            - Dietary Restrictions: {user_info['dietary_restrictions'].values[0]}
            - Allergies: {user_info['allergies'].values[0]}
            - Favorite Food: {user_info['favourite_food'].values[0]}
            - Most Disliked Food: {user_info['dislike_food'].values[0]}
            - Preferred Payment Method: {user_info['preferred_payment'].values[0]}
            - Prefered Restaurant Style: {user_info['restaurant_style'].values[0]}
            - Preferred Cuisine Type: {user_info['cuisine_type'].values[0]}
            - Typical Lunch Hour: {user_info['lunch_hour'].values[0]}
            - Typical Dinner Hour: {user_info['dinner_hour'].values[0]}
            - Normal Price Range the user is willing to pay per meal per person in euros: {user_info['normal_price_range'].values[0]}
            - The user is a smoker: {user_info['smoker_n'].values[0]}"""
            if st.session_state['username'] in personality_questionnaire['username'].values:
                user_info_formatted += f"""
                - Food Personality Type: {personality_questionnaire[personality_questionnaire['username'] == st.session_state['username']]['personality'].values[0]}"""
            return user_info_formatted
        else:
            return 'User Information Not Available'
    else:
        return 'User Information Not Available'
    
def get_data_match(data, word, col_to_match):
    nlp = spacy.load("en_core_web_md")

    word_embedding = nlp(word).vector
    similarities = {}
    for token in list(data[col_to_match].unique()):
        token_embedding = nlp(token).vector
        similarities[token] = cosine_similarity([word_embedding], [token_embedding])[0][0]

    return max(similarities, key=similarities.get)
    

def filter_schedule(restaurants, dinner_hour = None, lunch_hour = None):
    def contains_time_interval(schedule):
        if schedule in ['Closed', 'Not Available']:
            return False
        schedule_dict = {}
        try:
            schedule_dict = ast.literal_eval(schedule)
        except (SyntaxError, ValueError):
            pass

        for day_schedule in schedule_dict.values():
            if day_schedule == 'Closed':
                continue
            times = day_schedule.split(', ')
            for time in times:
                start, end = map(pd.to_datetime, time.split(' - '))
                if dinner_hour and lunch_hour:
                    if (start <= dinner_start <= end) or (start <= dinner_end <= end) or (start <= lunch_start <= end) or (start <= lunch_end <= end):
                        return True
                elif dinner_hour:
                    if (start <= dinner_start <= end) or (start <= dinner_end <= end):
                        return True
                elif lunch_hour:
                    if (start <= lunch_start <= end) or (start <= lunch_end <= end):
                        return True
                else:
                    return False
        return False

    dinner_start, dinner_end = map(pd.to_datetime, dinner_hour.split(' - '))
    lunch_start, lunch_end = map(pd.to_datetime, lunch_hour.split(' - '))

    filtered_restaurants = []
    for index, row in restaurants.iterrows():
        if contains_time_interval(row['schedule']):
            filtered_restaurants.append(row['name'])

    return filtered_restaurants

def get_personality(username):
    personality_questionnaire = pd.read_csv('data/training_answers/perturbed_total_answers.csv')
    if username in personality_questionnaire['username'].values:
        return personality_questionnaire[personality_questionnaire['username'] == username]['personality'].values[0]
    else:
        return 'Not Available'
    



# ------------------------ Relevant Variables ------------------------#

identification_vars = get_identification_and_user()
profile_vars = get_profile()
pattern = r"Username:\s*([^\s|]+)"
matches = re.search(pattern, identification_vars)

if type(matches) != type(None):
    username = matches.group(1)
    personality_type = get_personality(username)
else:
    username = 'Not Available'
    personality_type = 'Not Available'


# ------------------------ Prompt Templates ------------------------#


question_answer_template = """
TASK:
You are Filomena, a virtual assistant specialized in recommending restaurants for FlavourFlix users. \
Your role involves answering any question provided by the user about FlavourFlix and all of its functionalities, as well as 
help the user navigate the platform by answering any doubt. \
Your responses should be friendly, casual, yet professional. 

INSTRUCTION:
You will receive a chat history between the ChatBot and the user, and a final query from the user. \
Your job is to answer the user's question based on the provided context, the user question, and the chat history. \
If you cannot answer the question, you should return a message saying that you cannot answer the question.

Context:
{context} 
Chat History:
{chat_history}
User: 
{question}
Chatbot:
"""



instructions = {
                '[INSTRUCTION: Identification]': 
                 {'instruction description': """CONTEXT: You are Filomena, a virtual assistant talking with a FlavourFlix user. \
                        Assume a friendly, casual and professional tone. Greet the user. """,
                    'when to use': "When the user greets the ChatBot and the content of the last message from the assistant is empty."},


                 '[INSTRUCTION: Question]':
                 {'instruction description': question_answer_template, 
                  'when to use': """For non-restaurant-related questions (e.g., about FlavourFlix or the virtual assistant)""" },

                  '[INSTRUCTION: Restaurant Description]': 
                  {'instruction description': f"""Find the restaurant with the closest name of the query in the data and \
                                                    return its description using the function get_information.""",
                    'when to use': """When the user inquires about a specific restaurant by name. CAUTION: 
                                                "The Adventurer", "Fine Dining Connoiser", "Comfort Food Lover", "Low Cost Foodie" \
                                                    and "Conscious Eater" are not restaurant names."""},
                '[INSTRUCTION: What is my personality]': 
                {'instruction description': f"""CONTEXT: You are Filomena, a virtual assistant talking with a FlavourFlix user. \
                                                          Your role involves deciphering which personality type the user has based on \
                                                            the user's answers to the personality questionnaire.""",
                                                          'when to use': """When the user asks about their FlavourFlix personality type."""},
                '[INSTRUCTION: Determine the Personality]': 
                {'instruction description': f"""CONTEXT: You are Filomena, a virtual assistant talking with a FlavourFlix user. \
                                                          Your role involves deciphering which personality type the user has based on \
                                                            the user's answers to the personality questionnaire. """,
                'when to use': """When the user responds to a questionnaire about their 
                                                          dining preferences to find their personality type."""},
                '[INSTRUCTION: Get Restaurant Recommendation]': 
                {'instruction description': f"""CONTEXT: You are Filomena, a virtual assistant talking with a FlavourFlix user. 
                                                             You are focused on providing restaurant recommendations to the user. 
                                                             Your role involves obtaining the appropriate user preferences to feed into the recommendation algorithm. 
                                                             Assume a friendly, casual and professional tone.""",
                "when to use": """When the user specifically states that they want a restaurant recommendation and have not yet provided their preferences \
                                                            OR when the user states that they are not satisfied with the previous restaurant suggestion."""},
                '[INSTRUCTION: Get Recommendation Preferences]': 
                {'instruction description': f"""CONTEXT: You are Filomena, a virtual assistant talking with a FlavourFlix user.
                                                                You are focused on accurately dealing with user inputs to provide them with restaurant recommendations.""",
                "when to use": """When the user is asked about their preferences for a restaurant recommendation and provides with their personal preferences and tastes."""},}


instruction_identifier = """CONTEXT: You are a bot which identifies the instruction to be performed by a different virtual assistant. """



prepare_question_qa_template = """
Context: You are preprocessing general questions to be answered by the virtual assistance of the restaurant-recommendation plaform FlavourFlix. 
You are preprocessing the questions such that the virtual assistant has an easier time answering them. You will receive an 'Original prompt' 
and you must output a 'Refined prompt'. """

prepare_restaurant_question_template = """
Context: You are preprocessing restaurants-driven questions to be answered by the virtual assistance of the restaurant-recommendation plaform FlavourFlix.
You are preprocessing the questions such that the virtual assistant can accurately find the restaurant the original prompt mentions.
You will receive an 'Original prompt'
and you must output 'Restaurant Name'. \n
"""

personality_finder_system = """Context: You are FlavourFlix' virtual assistant. You are tasked with finding the personality type of the user.
                You will receive a 'Chat History' and a 'Query'. You must output the personality type of the user if possible. \n   """

questionnaire =  {"Willingness to Try Exotic Foods":"I am open to trying unfamiliar and exotic dishes.", 
             "Importance of Food Presentation":"The presentation and plating of my meal is very important.",
             "Value for Money in Meals":"I prioritize getting good value for price when choosing a meal.",
             "Preference for Gourmet Restaurants":"I prefer dining at high-end gourmet restaurants.",
             "Interest in Nutritional Content": "I pay a lot of attention to the nutritional content and health benefits of my meals.",
             "Frequency of Eating Home-Cooked Meals": "I often opt for home-cooked meals over dining out.",
             "Desire for New Culinary Experiences": "It is important to me to consistently explore new culinary experiences.",
             "Preference for Organic or Diet-Specific Foods": "I often incorporate organic or diet-specific foods (e.g., vegan, keto) in my meals.",
             "Enjoyment of Traditional or Familiar Foods": "I mostly enjoy eating traditional and/or familiar dishes.",
             "Willingness to Spend on High-Quality Ingredients": "I am willing to spend extra if it means getting high-quality ingredients.",}

personality_questionnaire_retrieval = f"""INSTRUCTIONS:
Present the following `questions` to the user, whose values will serve as input for a classification model:
{questionnaire}

The answers should be on a scale from 1 to 5, where 1 is "Strongly Disagree" and 5 is "Strongly Agree".
You also must add an final annotation <<<CLASSIFICATION_ON>>>
Get the values provided and generate a dictionary with the identifier of the question as the key and the value with the number provided by the user. 

Example of your request message to the user (for simplicity, shown with only 3 questions but you should ask all 10):
<message>
Yes, I can find your personality. To do that, I need you two answer the following questions, on a scale from 1 to 5, where \
     1 is "Strongly Disagree" and 5 is "Strongly Agree". 
a) "I am open to trying unfamiliar and exotic dishes."
b) "The presentation and plating of my meal is very important."
c) "The presentation and plating of my meal is very important."

<<<CLASSIFICATION_ON>>>
</message>
"""



prompt_templates = {'Instructions': instructions,
                     'Instruction Identification': instruction_identifier, 
                     'Preparing Questions': {'question_answer': prepare_question_qa_template, 
                                             'restaurant_description': prepare_restaurant_question_template},
                    'Personality Finder': {'system_config': personality_finder_system,
                                            'questionnaire_retrieval': personality_questionnaire_retrieval},
                    'Restaurant Recommendation': {'system_config': instructions['[INSTRUCTION: Get Restaurant Recommendation]']['system_config'],
                                                  
                                           }}