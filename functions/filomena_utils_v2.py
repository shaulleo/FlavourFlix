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
    

instructions = {
                '[INSTRUCTION: Identification]': 
                 {'description': """The assistant should greet the user.""",
                  'when to use': """When the user greets the assistant and the content of the last message from the assistant is empty."""},

                 '[INSTRUCTION: Question]':
                 {'description': """The assistant should answer the question of the user if they can.""", 
                  'when to use': """When the user asks non-restaurant-related questions (e.g. a question about a person, about FlavourFlix, about the virtual assistant or about portuguese gastronomic culture).""" },

                '[INSTRUCTION: Restaurant Description]': 
                 {'description': f"""The assistant should provide with a description of the restaurant in the `query`.""",
                  'when to use': """The user inquires about a specific restaurant, providing atleast the name of the restaurant. CAUTION: "The Adventurer", "Fine Dining Connoiser", "Comfort Food Lover", "Low Cost Foodie" and "Conscious Eater" are not restaurant names. CAUTION2: Do not confuse people names with restaurant names: e.g. "Madalena Frango" is not a restaurant. She is one of the founders of FlavourFlix.. CAUTION3: Do not confuse names of dishes with names of restaurants."""},
                                 }


# extras = {               '[INSTRUCTION: What is my personality]': 
#                 {'instruction description': f"""CONTEXT: You are Filomena, a virtual assistant talking with a FlavourFlix user. \
#                                                           Your role involves deciphering which personality type the user has based on \
#                                                             the user's answers to the personality questionnaire.""",
#                                                           'when to use': """When the user asks about their FlavourFlix personality type."""},


#                 '[INSTRUCTION: Determine the Personality]': 
#                 {'instruction description': f"""CONTEXT: You are Filomena, a virtual assistant talking with a FlavourFlix user. \
#                                                           Your role involves deciphering which personality type the user has based on \
#                                                             the user's answers to the personality questionnaire. """,
#                 'when to use': """When the user responds to a questionnaire about their 
#                                                           dining preferences to find their personality type."""},


#                 '[INSTRUCTION: Get Restaurant Recommendation]': 
#                 {'instruction description': f"""CONTEXT: You are Filomena, a virtual assistant talking with a FlavourFlix user. 
#                                                              You are focused on providing restaurant recommendations to the user. 
#                                                              Your role involves obtaining the appropriate user preferences to feed into the recommendation algorithm. 
#                                                              Assume a friendly, casual and professional tone.""",
#                 "when to use": """When the user specifically states that they want a restaurant recommendation and have not yet provided their preferences \
#                                                             OR when the user states that they are not satisfied with the previous restaurant suggestion."""},


#                 '[INSTRUCTION: Get Recommendation Preferences]': 
#                 {'instruction description': f"""CONTEXT: You are Filomena, a virtual assistant talking with a FlavourFlix user.
#                                                                 You are focused on accurately dealing with user inputs to provide them with restaurant recommendations.""",
    
#                 "when to use": """When the user is asked about their preferences for a restaurant recommendation and provides with their personal preferences and tastes."""}}


#Prompts para a identificação de instruções (peça central da Filomena)
instruction_identifier = {'system_configuration': f"""You are a Bot that helps categorize user queries (query) into different types of instructions. Your role is to be able to identify the type of instruction based on guidelines. You respond in a very simple and direct way, always with the following output: [Instruction: Instruction Identifier] | query""",
                           'task': f"""TASK: Your job is to assign an Instruction Identifier based on the user input `QUERY` and the last message from a  chat history `CHAT HISTORY`. You will receive a description about each Instruction Identifier in `CONTEXT`. OUTPUT: You will return the answer in the following format:[Instruction: Instruction Identifier] | query `CONTEXT`: {instructions} """ }

#Prompts para dar greeting ao utilizador
greeter_prompts = {'system_configuration': f"""You are a Bot named Filomena that works for FlavourFlix, speaking with a human. Your role is to greet the human in a casual, friendly and professional way""",
                   'task': f""" TASK: Greet the user by their username or first name (`IDENTIFICATION`), if it exists (is different from "No Identification Provided"). Otherwise, greet the user as "Fellow Foodie". Introduce yourself as Filomena - FlavourFlix' virtual assistant. Ask the user what they need your help with. `IDENTIFICATION`:""" + identification_vars}


qa_bot_prompts = {'qa_answerer': """INSTRUCTION: You are Filomena, a virtual assistant specialized in recommending restaurants for FlavourFlix users. Your role involves answering any question provided by the user about FlavourFlix, its functionalities and contributors, portuguese gastronomy, as well as help the user navigate the platform by answering any doubt. Your responses should be friendly, casual, yet professional. 
TASK: Use the information indicated in `CONTEXT` to answer the user's question. The question is defined by the `USER`. To answer it, you will receive a chat history between an assistant and the user. The chat history is defined by `CHAT HISTORY`.
Your job is to answer the user's question based on the provided `CONTEXT`, the `USER` question, and the `CHAT HISTORY`. If you cannot answer the question, you should specifically state that it is not possible to answer the question.
                    `CONTEXT`:
                    {context} 
                    `CHAT HISTORY`:
                    {chat_history}
                    `USER`: 
                    {question}
                    """,
                'question_preparer': {'system_configuration': """INSTRUCTION: You are a Bot that preprocesses questions `QUESTION` to be answered by a virtual assistant. You must reformulate the questions - if necessary - such that the virtual assistance has an easier time answering them based on document retieval. You will receive a `QUESTION` and you must output a `REFINED QUESTION`.""",
                            'task': """TASK: Reformulate the question `QUESTION` such that the virtual assistant has an easier time answering it based on document retrieval. """}}


