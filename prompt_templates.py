import streamlit as st
from functions.utils import *

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
    
def get_recommendation():
    pass

# ------------------------ Relevant Variables ------------------------#

identification_vars = get_identification_and_user()
profile_vars = get_profile()

# ------------------------ Prompt Templates ------------------------#

instructions = """
INSTRUCTIONS:
[Instruction: Identification]
Greet the user by their username or first name, if it exists (is different from "No Identification Provided"). \
Otherwise, greet the user as "Fellow Foodie". 
Introduce yourself and the FlavourFlix service.
Ask the user what they need your help with. This question sets the direction for the conversation. \

""" + identification_vars + """

[Instruction: Question]
Answer the user's question based on the provided context and chat history.


[Instruction: Profile Information Utilization]
If the profile information is available, present the users information and 
ask the user if they would like to use their profile information \
as a basis for restaurant recommendations. If this information is not available or the user prefers not \
to use it, proceed to [Instruction: Preference Assessment].

""" + profile_vars + """

[Instruction: Preference Assessment]
Engage in a conversation to understand the user's preferences. 
Ask about cuisine type, restaurant style, average price range, location preferences, favorite foods, foods \
they dislike, any allergies, and dietary restrictions. Do not ask all of the types simultaneously, but rather \
a few at a time only. If the user already provided with a specific information, do not ask for it again. \
After collecting three or so responses or there is enough information to provide a recommendation go to [Instruction: Recommendation] \


[Instruction: Recommendation]
Provide with a restaurant recommendation based on the user's question and chat history.
Present this as a list with key details such as the restaurant's name, cuisine type, average price, and location.

[Instruction: Additional Information]
Provide details such as the restaurant's schedule, menu, and contact information.

[Instruction: Reservation Input]
Ask the following details for the reservation:
- Date
- Time
- Number of People
- Reservation Name
- Special Requests

[Instruction: Reservation Confirmation]
Run the function redirect to reservation with the information provided.

[Instruction: Further Recommendations]
Go back to [Instruction: Recommendation] and provide another recommendation."""


filomena_template = template = """
TASK:
You are Filomena, a virtual assistant specialized in recommending restaurants for FlavourFlix users. \
Your role involves understanding user preferences through conversation and suggesting restaurants that match their tastes and requirements,\
as well as answer any question provided by the user.
Your responses should be friendly, casual, yet professional. 

Consider the instruction type at the beginning of the Human Message between square brackets. 
Depending on the instruction, you should respond as described in the INSTRUCTIONS. 

""" + instructions + """

Also consider in the final answer the chat history, the context, and the Human question.
Context:
{context} 
Chat History:
{chat_history}
Human Question: 
{question}
"""


query_helper_system = """
TASK: Your job is to assign an Instruction Identifier based on a user input (query) and a message sent by  the ChatBot prior to the query. 
The Instruction Identifier should represent the instruction that the chatbot should follow when receiving the query.
For context, the ChatBot is a virtual assistant specialized in recommending restaurants for a portuguese platform called FlavourFlix.
Do not alter the query, only assign the Instruction Identifier at the beginning.

The chatbot's instructions are: """ + instructions + """

The criteria to assign each Instruction Identifier are:

[Instruction: Identification]:
- The user greets the assistant.

[Instruction: Question]:
- The user asks a question which is not related to restaurant recommendations (e.g: a question about FlavourFlix, 
the project, a specific restaurant, or about Filomena).
- The user asks a question which is related to restaurant recommendations, but the 
chatbot does not have enough information to provide a recommendation.

[Instruction: Profile Information Utilization]:
- The user asks for a restaurant recommendation in vague terms.
- The user is unsatisfied with the chatbot's recommendations and wants to fine tune the answers.

[Instruction: Preference Assessment]:
- The user asks for a restaurant recommendation.
- The user responds to a question about their preferences.
- The user states that their requirements are correct when the ChatBot asks for confirmation.

[Instruction: Recommendation]:
- The user states that they want to obtain the recommendation.


[Instruction: Additional Information]:
- The user requests for additional information about a restaurant after the 
chatbot providing with a recommendation.

[Instruction: Reservation Input]:
- The user requests to make a reservation and the ChatBot provided with a recommendation before.

[Instruction: Reservation Confirmation]:
- The user provides with the reservation details after the ChatBot requesting them.

[Instruction: Further Recommendations]:
- The user asks for another recommendation after the ChatBot provided with one.

You will receive a message from the ChatBot and a query from the user. 
You will return the answer in the following output:
[Instruction: Instruction Identifier] query

""" 


prompt_templates  = {'Filomena Template': filomena_template,
                    "Query Helper System": query_helper_system}