import streamlit as st
from functions.utils import *
from sklearn.metrics.pairwise import cosine_similarity 
import spacy
import numpy as np
import pandas as pd
from unidecode import unidecode
import re
import random
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
    

def get_data_match(data, word, col_to_match, method='dot'):
    nlp = spacy.load("en_core_web_md")
    data_match = data[data[col_to_match].str.contains(word)].head(1)
    if len(data_match) == 0:
        word_clean = unidecode(word)
        word_clean = word_clean.lower()
        similarities = {}
        for possible_match in list(data[col_to_match].unique()):
            possible_match_clean = unidecode(possible_match)
            possible_match_clean = possible_match_clean.lower()
            if word_clean in possible_match_clean:
                data_match = data[data[col_to_match] == possible_match].head(1)
                if len(data_match) == 0:
                    continue
                else:
                    data_match = data_match[col_to_match].values[0]
                    return data_match
            else:
                word_embedding = nlp(word_clean).vector
                if ' - ' in possible_match and ' - ' not in word:
                    possible_match_clean = possible_match_clean.split(' - ')[0]
                    possible_match_embedding = nlp(possible_match_clean).vector
                else:
                    possible_match_embedding = nlp(possible_match).vector
                if method == 'dot':
                    dot_product = np.dot(word_embedding, possible_match_embedding)
                    similarities[possible_match] = dot_product
                elif method == 'cosine':
                    cosine_score = cosine_similarity([word_embedding], [possible_match_embedding])[0][0]
                    similarities[possible_match] = cosine_score
                else:
                    print('Method not recognized')
                    return None
                data_match = max(similarities, key=similarities.get)
    else:
        data_match = data_match[col_to_match].values[0]
    return data_match   


def filter_schedule(restaurants, time_slot=None):
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
                if (start <= time_start <= end) or (start <= time_end <= end):
                    return True
                else:
                    return False
        return False

    time_start, time_end = map(pd.to_datetime, time_slot.split(' - '))

    filtered_restaurants = []

    for index, row in restaurants.iterrows():
        if contains_time_interval(row['schedule']):
            filtered_restaurants.append(row.to_dict())

    return pd.DataFrame(filtered_restaurants)


def get_personality(username):
    personality_questionnaire = pd.read_csv('data/training_answers/perturbed_total_answers.csv')
    if username in personality_questionnaire['username'].values:
        return personality_questionnaire[personality_questionnaire['username'] == username]['personality'].values[0]
    else:
        return 'Not Available'
    

def get_preferences(personality):
    questions = {'location': 'Where is the city where you eat?',
                 'nationality': 'What is the nationality of the food you are looking for?',
                 'cuisine': 'What cuisine do you want to eat?',
                 'style': 'What restaurant style do you prefer?',
                 'budget': 'What is your budget in euros, per meal?',
                 'dinner_hour': 'What time interval do you want to have dinner? Provide in the format: "HH:MM - HH:MM"',
                 'lunch_hour': 'What time interval do you want to have lunch? Provide in the format: "HH:MM - HH:MM"',
                 'favourite_meal': 'What meal do you feel like having?',
                'preference': 'What do you priorize the most: price, ambience, food quality or service quality?'}
    if personality != 'Not Available':
        return [f'I see that you belong to the food personality {personality}',questions['location']]
    else:
        possible_questions = list(questions.keys())
        possible_questions.remove('location')
        selected = random.sample(possible_questions, 2)
        selected = [questions[sel] for sel in selected]
        selected.append(questions['location'])
        return selected

    
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

instructions = {
                '[INSTRUCTION: Identification]': 
                 {'description': """The assistant should greet the user.""",
                  'when to use': """When the user greets the assistant (e.g. Hello!) and the content of the last message from the assistant is empty."""},

                 '[INSTRUCTION: Question]':
                 {'description': """The assistant should answer the question of the user if they can.""", 
                  'when to use': """When the user asks non-restaurant-related questions (e.g. a question about a person, about FlavourFlix, about the virtual assistant or about portuguese gastronomic culture).""" },

                '[INSTRUCTION: Restaurant Description]': 
                 {'description': f"""The assistant should provide with a description of the restaurant in the `query`.""",
                  'when to use': """The user inquires about a specific restaurant, providing atleast the name of the restaurant. CAUTION: "The Adventurer", "Fine Dining Connoiser", "Comfort Food Lover", "Low Cost Foodie" and "Conscious Eater" are not restaurant names. CAUTION2: Do not confuse people names with restaurant names: e.g. "Madalena Frango" is not a restaurant. She is one of the founders of FlavourFlix.. CAUTION3: Do not confuse names of dishes with names of restaurants."""},

                '[INSTRUCTION: Prepare Restaurant Recommendation]':
                {'description': f"""The assistant should ask the user for the information necessary to generate a restaurant recommendation.""",
                                'when to use': """The user asks the assistant for a restaurant recommendation."""},
                '[INSTRUCTION: Deliver Restaurant Recommendation]':
                {'description': f"""The assistant should deliver a restaurant recommendation.""",
                                'when to use': """The user provides with information about their dining preferences and location after the assistant requests them for a restaurant recommendation."""},

                '[INSTRUCTION: What is my personality]': 
                {'description': f"""The assistant should ask the user a series of questions to determine their food/FlavourFlix personality if they do not have access to the user's food/FlavourFlix personality yet.""",
                                'when to use': """The user asks the assistant specifically what their food personality or FlavourFlix personality is."""},

                '[INSTRUCTION: Questionnaire Answers]':
                {'description': f"""The assistant should find the user's food/FlavourFlix personality based on the values provided by the user for each question.""",
                                'when to use': """The user provides with the answers (from 1 to 5 or Strongly Agree to Strongly Disagree) to the 10 questions from the FlavourFlix' questionnaire after the assistant presents it."""},

                '[INSTRUCTION: Unsatisfaction]': 
                {'description': f"""The assistant should apologize for not meeting the user's expectation and ask how can they better serve the user's interests.""",
                                'when to use': """The user expresses dissatisfaction, dislike, irritability, frustration, annoyance with the prior response or the user states that the assistant did not do what was asked."""},
}

#Prompts para a identificação de instruções (peça central da Filomena)
instruction_identifier = {'system_configuration': f"""You are a Bot that helps categorize user queries `QUERY` into different types of instructions. Your role is to be able to identify the type of instruction based on guidelines. You respond in a very simple and direct way. `OUTPUT`:  [INSTRUCTION: Instruction Identifier] | `QUERY`""",
                           'task': f"""TASK: Your job is to assign an Instruction Identifier based on the user input `QUERY` and the last message from a  chat history `CHAT HISTORY`. You will receive a description about each Instruction Identifier (`CONTEXT`). `CONTEXT`: {instructions}. `OUTPUT`: You will return the answer in the following format:[INSTRUCTION: Instruction Identifier] | `QUERY` """ }

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


restaurant_desc_bot_prompts = {'question_preparer': {'system_configuration': """INSTRUCTION: You are a Bot that preprocess questions `QUESTIONS` about restaurants to be answered by a virtual assistant. You are preprocessing the questions such that the virtual assistant can accurately find the restaurant mentioned in the `QUESTION`. You will receive a `QUESTION` and you must output a `REFINED QUESTION`.""",
                            'task': """TASK: Extract the restaurant name (`RESTAURANT NAME`) mentioned in the question `QUESTION`. OUTPUT: `RESTAURANT NAME`. """},}



restaurant_recommender_prompts = {'input_retriever':  {'system_configuration': """INSTRUCTION: You are a bot that works for FlavourFlix' restaurant recommendation department. Your job is to receive sentences and condense them into a given format. """, 
                                                        'task_make_question': f"""TASK: Consider the sentences in `CONTEXT`. Incorporate them into a `PHRASE` that is coherent and readable for a human, as if you were answering to a human who just stated to you that they want to receive a restaurant recommendation. You must assume a friendly and casual tone.""",
                                                        'task_format_inputs': f"""TASK: Consider the sentences in `CONTEXT`. Extract the information within them and present it as a dictionary. The keys of the dictionary are described in `KEYS`. If the information is not available, the value of the key should be None. `KEYS`: [personality, location, nationality, cuisine_type, restaurant_style, price_range, dinner_hour, lunch_hour, favourite_food, priority] """,}}
                                                      
personality_bot_prompts = {'input_retriever': {'system_configuration': 'INSTRUCTION: You are a friendly and helpful assistant called Filomena. A human just asked you if you could classify their personality type. Now your task is to make a bunch of questions to the human, that will serve as input for a classification model. Afterwards their answers will be preprocessed.',
                                               'task_make_question': f"""TASK: Present the following `QUESTIONS`to the user without any modification. State that the answers should be on a scale from 1 to 5, where 1 corresponds to "Strongly Disagree" and 5 is "Strongly Agree". Also suggest that the user should respond to them all at once. Inform the user that answering these questions is necessary to determine the user's personality and that they may  respond to the questions directly in the designated app page OR with you, Filomena. `QUESTIONS`: {list(questionnaire.values())}""",
                                               'task_format_inputs': f"""Extract the answer values from `TEXT` and generate a dictionary with the question identifier (key of `QUESTIONS`) and the respective user answer. Note that if the user answer is a string, you should convert it to the corresponding number on a scale from 1 to 5. Do not include any newlines. `QUESTIONS`: {questionnaire} OUTPUT FORMAT: dict("question_identifier": "user_answer")"""}}


dissatisfaction_bot_prompts = {'system_configuration': """INSTRUCTION: You are a bot called Filomena that works for FlavourFlix' customer service department. Your job is to receive expressions of unsatisfaction from an user that ensure the user that their inconvenience will be solved. """,
                               'task': """TASK: Consider the message in `USER INPUT`. Apologize to the user not being able to meet their expectations, and justify yourself by stating that you are still learning. Plead for their patience. Ask how may you assist them better.""",}