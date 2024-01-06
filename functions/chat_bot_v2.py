from functions.filomena_utils_v2 import *
from functions.utils import *
from openai import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.memory import ConversationBufferMemory
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain import hub
from langchain.agents import AgentExecutor, create_structured_chat_agent
from functions.utils import *
from openai import OpenAI
from langdetect import detect
from functions.location import *
from functions.preprocessement import *
from langchain.agents import tool
from langchain.agents import load_tools, initialize_agent
from langchain.agents import AgentType
import pickle
from unidecode import unidecode 
from functions.preprocessement import *


#  ----------------------------- AGENT TOOLS ----------------------------- #

@tool
def get_restaurant_info(restaurant_name: str):
    """Gathers all the restaurant information from the FlavourFlix restaurant 
    restaurant_database, based on the name of the restaurant.
    Parameters:
        - restaurant_name (str): The name of the restaurant exactly as 
        it appears in the restaurant_data.
    Returns:
        - result (str): A string with all the information 
        about the restaurant.
    """
    restaurant_restaurant_data = pd.read_csv('data/preprocessed_restaurant_data.csv')
    restaurant_restaurant_data = restaurant_restaurant_data[restaurant_restaurant_data['name'] == restaurant_name].head(1)
    result = f"""Name: {restaurant_restaurant_data["name"].values[0]} \n /
    Cuisine Type: {restaurant_restaurant_data["cuisine"].values[0]} \n /
    Average Price: {restaurant_restaurant_data["averagePrice"].values[0]} \n /
    Location: {restaurant_restaurant_data["location"].values[0]} \n /
    Restaurant Style: {restaurant_restaurant_data["style"].values[0]} \n /
    Restaurant Schedule: {restaurant_restaurant_data["schedule"].values[0]}"""
    return result

def personality_based_recommendation(personality: str, location:str=None):
    """Gets restaurant recommendations based on the user's personality and loation if provided.
    Parameters:
        - personality (str): The user's personality. Can only be one of the following: 
                - [The Adventurer, Fine Dining Connoisseur, Low Cost Foodie, Conscious Eater, Comfort Food Lover].
        - location (str): The user's location.
    Returns:
        - rec_restaurants (DataFrame): A DataFrame with the recommended restaurants.
    """

    restaurant_data = pd.read_csv('data/preprocessed_restaurant_data.csv')

    #If we have access to the location preferece, we will filter the restaurants based on the location and nearby locations
    if location is not None:
        #Find the restaurants in the location
        equal_location = restaurant_data[restaurant_data['location'] == location]
        rec_restaurants = equal_location
        #Find the restaurants
        latitude, longitude = find_coordinates(location)
        # if latitude is not None and longitude is not None:
        #     selected_location = Location(latitude, longitude)
        #     restaurant_data = nearYou(selected_location, restaurant_data)
        #     restaurant_data['minutes_away_car'] = restaurant_data.apply(lambda row: selected_location.getDirections(row['latitude'], row['longitude'], ['driving'])['driving'].minutes, axis=1)
        #     near_location = restaurant_data[restaurant_data['minutes_away_car'] <= 20]
        #     rec_restaurants = pd.concat([near_location, equal_location], ignore_index=True)
        # else:
        #     rec_restaurants = equal_location
    else:
        rec_restaurants = restaurant_data            
        
    #Now we will filter the restaurants based on the personality
    if personality == 'The Adventurer':
        rec_restaurants = rec_restaurants[rec_restaurants['cuisine'].isin(['Peruvian', 'Lebanese', 'Iranian', 'Vietnamese', 'Fusion', 'Nepalese', 'Thai', 'Asian',
                        'Korean', 'Tibetan', 'Chinese', 'African', 'Syrian', 'Venezuelan', 'Indian', 'Japanese','South American',
                        'Argentinian', 'Mexican'])]
        rec_restaurants = pd.concat([rec_restaurants[rec_restaurants['style'] == 'Ethnic'], rec_restaurants[rec_restaurants['style'] != 'Ethnic']])
        rec_restaurants.sort_values(by=['foodRatingSummary'], ascending=False, inplace=True)

    
    elif personality == 'Fine Dining Connoisseur':
        rec_restaurants = rec_restaurants[rec_restaurants['style'].isin(['Fine Dining', 'Modern', 'View', 'Central Location', 'Brunch', 'Meetings'])] 
        rec_restaurants = rec_restaurants[(rec_restaurants['ambienceRating'] >= 8) & (rec_restaurants['serviceRating'] >= 8)]
        rec_restaurants.sort_values(by=['ambienceRatingSummary', 'serviceRatingSummary'], ascending=False, inplace=True)
    
    elif personality == 'Low Cost Foodie':
        #lowcost_rest = ['Street Food', 'Buffet', 'Brazilian', 'Not Available', 'Homemade', 'Family', 'Healthy',]
        #rec_restaurants = rec_restaurants[rec_restaurants['style'].isin(lowcost_rest) & (restaurant_data['averagePrice'] < 12) & (restaurant_data['promotions'] =! 'No Offers')]
        rec_restaurants = rec_restaurants[(rec_restaurants['promotions'] != 'No Offers')]
        rec_restaurants.sort_values(by=['averagePrice', 'foodRatingSummary'], ascending=[True, False], inplace=True)

    elif personality == 'Conscious Eater':
        conscious_cuisine = ['Mediterranean', 'Greek', 'Vegan', 'Vegetarian', 'Traditional']
        rec_restaurants = rec_restaurants[rec_restaurants['cuisine'].isin(conscious_cuisine)]
        rec_restaurants = pd.concat([rec_restaurants[(rec_restaurants['style'] == 'Healthy') | (rec_restaurants['style'] == 'Brunch')], 
                                     rec_restaurants[(rec_restaurants['style'] != 'Healthy') | (rec_restaurants['style'] != 'Brunch')]])
        rec_restaurants.sort_values(by=['foodRatingSummary'], ascending=False, inplace=True)
    
    if personality == 'Comfort Food Lover':
        comfort_cuisine = ['Traditional', 'American', 'Portuguese', 'Brazilian', 'Pizzeria', 'Mexican',
                            'Pub grub', 'Grilled', 'Spanish', 'Mediterranean', 'Italian', 'Meat', 'Steakhouse']
        rec_restaurants = rec_restaurants[rec_restaurants['cuisine'].isin(conscious_cuisine)]
        rec_restaurants = pd.concat([rec_restaurants[(rec_restaurants['style'] == 'Homemade') | (rec_restaurants['style'] == 'Healthy')], 
                                     rec_restaurants[(rec_restaurants['style'] != 'Homemade') | (rec_restaurants['style'] != 'Healthy')]])
        rec_restaurants.sort_values(by=['foodRatingSummary'], ascending=False, inplace=True)

    return rec_restaurants.head(5)

def user_preferences_recommendation(location: str=None, nationality: str= None, cuisine_type: str=None,
                                     restaurant_style: str = None, price_range: str=None, dinner_hour: str=None, 
                                     lunch_hour: str=None, favourite_food: str=None, preference: str='ratingValue'):
    
    """Gets restaurant recommendations based on the user's preferences.
    Parameters:
        - location (str):  The city the user wants to eat in.
        - nationality (str): Nationality of the food the user wants to eat.
        - cuisine_type (str): The type of cuisine the user wants to eat.
        - restaurant_style (str): The style of the restaurant the user wants to eat at.
        - price_range (str): The price value in euros the user is willing to pay per meal per person.
        - dinner_hour (str): The timeslot the user wants to have dinner in the format "HH:MM - HH:MM".
        - lunch_hour (str): The timeslot the user wants to have lunch in the format "HH:MM - HH:MM".
        - favourite_food (str): The specific dish or meal the user wants to eat.
        - preference (str): The user's preference. Can only be one of the following:
                - [ratingValue, averagePrice, ambienceRatingSummary, serviceRatingSummary, foodRatingSummary].
    Returns:
        - rec_restaurants (DataFrame): A DataFrame with the recommended restaurants.

    """
    
    restaurant_data = pd.read_csv('data/preprocessed_restaurant_data.csv')

    #If we have access to the location preferece, we will filter the restaurants based on the location and nearby locations
    if location is not None:
        #Find the restaurants in the location
        equal_location = restaurant_data[restaurant_data['location'] == location]
        rec_restaurants = equal_location
        #Find the restaurants
        latitude, longitude = find_coordinates(location)
        # if latitude is not None and longitude is not None:
        #     selected_location = Location(latitude, longitude)
        #     restaurant_data = nearYou(selected_location, restaurant_data)
        #     restaurant_data['minutes_away_car'] = restaurant_data.apply(lambda row: selected_location.getDirections(row['latitude'], row['longitude'], ['driving'])['driving'].minutes, axis=1)
        #     near_location = restaurant_data[restaurant_data['minutes_away_car'] <= 20]
        #     rec_restaurants = pd.concat([near_location, equal_location], ignore_index=True)
        # else:
            # rec_restaurants = equal_location
    else:
        rec_restaurants = restaurant_data  

    if len(rec_restaurants) > 5:
        #Now we will filter the restaurants based on the user preferences
        if cuisine_type is not None and nationality is not None:
            cuisine_match = get_data_match(restaurant_data, cuisine_type, 'cuisine')
            nationality_match = get_data_match(restaurant_data, nationality, 'cuisine')
            rec_restaurants = rec_restaurants[(rec_restaurants['cuisine'] == cuisine_match) | (rec_restaurants['cuisine'] == nationality_match)]
        elif cuisine_type is not None:
            cuisine_match = get_data_match(restaurant_data, cuisine_type, 'cuisine')
            rec_restaurants = rec_restaurants[(rec_restaurants['cuisine'] == cuisine_match) ]
        elif nationality is not None:
            nationality_match = get_data_match(restaurant_data, nationality, 'cuisine')
            rec_restaurants = rec_restaurants[(rec_restaurants['cuisine'] == nationality_match)]
    else:
        return rec_restaurants
    
    if len(rec_restaurants) > 5:
        if restaurant_style is not None:
            style_match = get_data_match(restaurant_data, restaurant_style, 'style')
            rec_restaurants = rec_restaurants[(rec_restaurants['style'] == style_match)]
    else:
        return rec_restaurants

    if len(rec_restaurants) > 5:
        if favourite_food is not None:
            if detect(favourite_food) == 'en':
                rec_restaurants[rec_restaurants['menu_en'].str.contains(favourite_food)]
            else:
                rec_restaurants[rec_restaurants['menu_pre_proc'].str.contains(favourite_food)]
        else:
            rec_restaurants = rec_restaurants
    else:
        return rec_restaurants
    
    if len(rec_restaurants) > 5:
        if price_range is not None:
            rec_restaurants[rec_restaurants['averagePrice'] <= price_range +4]
    else:
        return rec_restaurants

    if len(rec_restaurants) > 5:
        if lunch_hour is not None and dinner_hour is not None:
            rec_restaurants = filter_schedule(rec_restaurants, dinner_hour, lunch_hour)
        elif dinner_hour is not None:
            rec_restaurants = filter_schedule(rec_restaurants, dinner_hour, lunch_hour)
        elif lunch_hour is not None:
            rec_restaurants = filter_schedule(rec_restaurants, dinner_hour, lunch_hour)
    else:
        return rec_restaurants
    
    if preference == 'averagePrice':
        rec_restaurants = rec_restaurants.sort_values(by=['averagePrice'], ascending=True)
    else:
        rec_restaurants = rec_restaurants.sort_values(by=[preference], ascending=False)

    return rec_restaurants.head(5)
        

@tool
def get_recommendation(personality: str=None, location: str =None, nationality: str= None, cuisine_type: str=None,
                                     restaurant_style: str = None, price_range: str=None, dinner_hour: str=None, 
                                     lunch_hour: str=None, favourite_food: str=None, preference: str='ratingValue'):
    """Gets restaurant recommendations based on the user's personality or 
    personal preferences stated throughout the chat.
    Parameters:
        - personality (str): The user's personality. Can only be one of the following:
                - [The Adventurer, Fine Dining Connoisseur, Low Cost Foodie, Conscious Eater, Comfort Food Lover].
        - location (str):  The city the user wants to eat in.
        - nationality (str): Nationality of the food the user wants to eat.
        - cuisine_type (str): The type of cuisine the user wants to eat.
        - restaurant_style (str): The style of the restaurant the user wants to eat at.
        - price_range (str): The price value in euros the user is willing to pay per meal per person.
        - dinner_hour (str): The timeslot the user wants to have dinner in the format "HH:MM - HH:MM".
        - lunch_hour (str): The timeslot the user wants to have lunch in the format "HH:MM - HH:MM".
        - favourite_food (str): The specific dish or meal the user wants to eat.
        - preference (str): The user's preference. Can only be one of the following:
                - [ratingValue, averagePrice, ambienceRatingSummary, serviceRatingSummary, foodRatingSummary]. 
    Returns:
        - rec_restaurants (DataFrame): A DataFrame with the recommended restaurants.
    """
    if personality != None:
        recommendations = personality_based_recommendation(personality, location)
    else:
        recommendations = user_preferences_recommendation(location, nationality, cuisine_type,restaurant_style, price_range, dinner_hour, 
                                     lunch_hour, favourite_food, preference)
    return recommendations


def reduce_memory(memory: list):
    """Reduces the memory of the agent to avoid exceeding the maximum
    number of characters allowed by the OpenAI API.
    Parameters:
        - memory (list): The memory of the agent.
    Returns:
        - new_memory (list): The reduced memory of the agent.
    """
    new_memory = [memory[0]]
    new_memory.extend(memory[-3:])
    if len(str(new_memory)) > 3500:
        new_memory = [memory[0]]
        new_memory.extend(memory[-1:])
    return new_memory

# ----------------------------- AGENTS ----------------------------- #

class GPT_Helper:
    def __init__(self,
        OPENAI_API_KEY: str,
        system_behavior: str="",
        model: str="gpt-3.5-turbo"):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.messages = []
        self.model_messages = []
        self.model = model

        if system_behavior:
            self.messages.append({
                "role": "system",
                "content": system_behavior
            })

           
    def get_completion(self, prompt: str, temperature: float =0.0):
        """Get the completion of the prompt.
        Parameters:
            - prompt (str): The prompt to be completed.
            - temperature (float): The level of creativity of 
            the answer.
        Returns:
            - completion (str): The LLM's answer to the 
            prompt."""
        
        if len((self.model_messages)) <= 5:

            self.model_messages.append({"role": "user", "content": prompt})
            self.messages.append({"role": "user", "content": prompt})

            completion = self.client.chat.completions.create(
                model=self.model,
                messages= self.model_messages,
                temperature=temperature,
            )
            self.messages.append({"role": "assistant", "content": completion.choices[0].message.content})
            self.model_messages.append({"role": "assistant", "content": completion.choices[0].message.content})

            return completion.choices[0].message.content
        else:
            self.model_messages = reduce_memory(self.model_messages)
            return self.get_completion(prompt, temperature=temperature)
    

    def get_instruction(self, query: str, chat_history: list):
        """Get the instruction to be performed by the agent.
        Parameters:
            - query (str): The user's query.
            - chat_history (list): The chat history.
        Returns:
            - instruction (str): The instruction to be performed."""
        prompt = instruction_identifier['task'] + f"""
                        `QUERY`: {query}
                        `CHAT HISTORY`: {chat_history}""" 

        query_formatted = self.get_completion(prompt)
        if query not in query_formatted:
            query_formatted = f'{query_formatted} | {query}'
        return query_formatted



class QuestionAnsweringBot():

    def __init__(self):
        self.llm = ChatOpenAI(temperature=0.3, api_key=local_settings.OPENAI_API_KEY)
        self.memory = ConversationBufferMemory(memory_key="chat_history",  input_key="question")
        self.prompt = PromptTemplate(
            input_variables=["chat_history", "question", "context"], template= qa_bot_prompts['qa_answerer'])
        self.agent_chain = load_qa_chain(self.llm, chain_type="stuff", memory=self.memory, prompt=self.prompt)
        self.messages = []
        self.model_messages = []
    
    def load_documents(self, files: list):
        """Prepares, embedds, and loads the documents to be used by the 
        agent in a Vector restaurant_database.
        Parameters:
            - files (list): A list of file paths.
        Returns:
            - None
        """
        docs = []
        for file_path in files:
                loader = PyPDFLoader(file_path)
                docs.extend(loader.load())
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500,chunk_overlap=200)
        splits = text_splitter.split_documents(docs)
        embeddings = OpenAIEmbeddings()
        vectordb = FAISS.from_documents(splits, embeddings)
        self.vectordb = vectordb

    def initialize_qa(self, files: list):
        """Initializes the agent. by loading the
        documents that will be the basis of the answer.
        Parameters:
            - files (list): A list of file paths.
        Returns:
            - None
         """
        self.load_documents(files)

    def prepare_question(self, query:str):
        """Prepares the question to be answered by the agent.
        Parameters:
            - query (str): The question to be answered.
        Returns:
            - query_prepared (str): The question to be answered,
            after being prepared by the agent.
        """
        question_preparer = GPT_Helper(OPENAI_API_KEY=local_settings.OPENAI_API_KEY, 
                                       system_behavior = qa_bot_prompts['question_preparer']['system_configuration'])  
        query = f"""{qa_bot_prompts['question_preparer']['task']} `QUESTION`: {query} `REFINED QUESTION`: """
        query_prepared = question_preparer.get_completion(query)
        return query_prepared
    

    def generate_response(self, query):
        """Generates the response to the user's question based on 
        documents within the Vector restaurant_database.
        Parameters:
            - query (str): The question to be answered.
        Returns:
            - response (str): The answer to the user's question.
        """
        # retriever = 
        # retriever.get_relevant_documents(question)
        #self.vectordb.similarity_search(query_prepared, k=1),

        query_prepared = self.prepare_question(query)
        if len((self.model_messages)) <= 5:
            response = self.agent_chain( 
                {"input_documents": self.vectordb.max_marginal_relevance_search(query_prepared ,k=3),
                    "question": f'{query_prepared}', }, return_only_outputs=True)
            
            return response['output_text']
        else:
            self.model_messages = reduce_memory(self.self.model_messages)
            return self.generate_response(query)
        

class RestaurantDescriptionBot():
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0.3, api_key=local_settings.OPENAI_API_KEY, model='gpt-3.5-turbo')
        self.agent= initialize_agent([get_restaurant_info],
            self.llm,
            agent= AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            handle_parsing_errors=True,
            verbose = False)
        
    def prepare_question(self, query:str):
        """Prepares the question to be answered by the agent.
        Parameters:
            - query (str): The question to be answered.
        Returns:
            - query_prepared (str): The question to be answered,
            after being prepared by the agent."""
        
        restaurant_restaurant_data = pd.read_csv('data/preprocessed_restaurant_data.csv')

        question_preparer = GPT_Helper(OPENAI_API_KEY=local_settings.OPENAI_API_KEY, 
                                       system_behavior = restaurant_desc_bot_prompts['question_preparer']['system_configuration'])  
        query = restaurant_desc_bot_prompts['question_preparer']['system_configuration'] + f""" `QUERY`: {query} `RESTAURANT NAME`: """
                
        restaurant_name = question_preparer.get_completion(query)
        restaurant_name = get_data_match(restaurant_restaurant_data, restaurant_name, 'name')
        query_prepared = f"""Tell me about the restaurant '{restaurant_name}'."""
        return query_prepared
        
        
    def generate_response(self, query):
        """Generates the response to the user's question based on
        documents within the Vector restaurant_database.
        Parameters:
            - query (str): The question to be answered.
        Returns:
            - response (str): The answer to the user's question."""
        query_prepared = self.prepare_question(query)
        response = self.agent(query_prepared)
        return response['output']


class RestaurantRecommendationBot():
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0.0, api_key=local_settings.OPENAI_API_KEY, model='gpt-3.5-turbo')
        self.tools = [get_recommendation]
        self.hub_prompt = hub.pull("hwchase17/structured-chat-agent")
        self.agent = create_structured_chat_agent(self.llm, self.tools, self.hub_prompt)
        self.agent_executor = AgentExecutor(agent= self.agent, tools=self.tools, verbose=False, handle_parsing_errors=True)
        self.input_obtainer = GPT_Helper(OPENAI_API_KEY=local_settings.OPENAI_API_KEY, 
                                       system_behavior = restaurant_recommender_prompts['input_retriever']['system_configuration'])

    def generate_recommendation(self, query: str):
        """Generates the recommendation to the user's question based on
        their preferences or personality type.
        Parameters:
            - query (str): The user's query where they specify their preferences or personality type.
        Returns:
            - response (str): The restaurant recommendation to the user's question.
        """
        inputs = self.format_inputs(query)
        prompt = restaurant_recommender_prompts['restaurant_recommender']['task'] + f""" USER INPUTS: {inputs}"""
        response = self.agent_executor.invoke({"input": query})
        return response['output']
    
    def ask_for_inputs(self):
        """Asks the user for their preferences or personality type when asked to recommend a restaurant.
        Parameters:
            - None
        Returns:
            - response (str): The user's answer on their preferences or personality type.
        """
        prompt = restaurant_recommender_prompts['input_retriever']['task_ask']
        response = self.input_obtainer.get_completion(prompt)
        return response
    
    def format_inputs(self, query: str):
        """Formats the user's inputs to be used by the agent.
        Parameters:
            - query (str): The user's query where they specify their preferences or personality type.
        Returns:    
            - response (str): The user's inputs formatted to be used by the agent."""
        
        prompt = restaurant_recommender_prompts['input_retriever']['task_format'] + f""" USER INPUTS: {query} """
        response = self.input_obtainer.get_completion(prompt)
        return response


# ----------------------------- Filomena ----------------------------- #

class Filomena():
    def __init__(self):
        self.core_piece = GPT_Helper(OPENAI_API_KEY=local_settings.OPENAI_API_KEY, 
                                     system_behavior = instruction_identifier['system_configuration'])
        self.llm = ChatOpenAI(temperature=0, 
                              api_key=local_settings.OPENAI_API_KEY)
        self.messages = []
        self.model_messages = []
        self.question_agent = QuestionAnsweringBot()
        self.restaurant_descriptor_agent = RestaurantDescriptionBot()
        self.restaurant_recommendation_agent = RestaurantRecommendationBot()


    def greet(self):
        """Greets the user.
        Parameters:
            - None
        Returns:
            - response (str): The greeting to the user.
        """
        greeter = GPT_Helper(OPENAI_API_KEY=local_settings.OPENAI_API_KEY, system_behavior = greeter_prompts['system_configuration'])
        
        response = greeter.get_completion(greeter_prompts['task'], temperature=0.9)
        self.model_messages.extend(greeter.messages[-1:])
        self.messages.extend(greeter.messages[-1:])
        return response
    

    def perform_instruction(self, query, chat_history):
        """Performs the instruction given by the user.
        Parameters:
            - query (str): The user's query.
            - chat_history (list): The chat history.
        Returns:
            - response (str): The answer to the user's query.
        """
        to_perform = self.core_piece.get_instruction(query, chat_history)
        pattern = r'\[INSTRUCTION: [^\]]+\]'
        match = re.search(pattern, to_perform)
        if match:
            instruction_name = match.group()
        else:
            instruction_name = 'Not Available'

        if instruction_name == '[INSTRUCTION: Identification]':
            response = self.greet()
        elif instruction_name == '[INSTRUCTION: Question]':
            response = self.question_agent.generate_response(query)
        elif instruction_name == '[INSTRUCTION: Restaurant Description]':
            response = self.restaurant_descriptor_agent.generate_response(query)
        elif instruction_name == '[INSTRUCTION: Prepare Restaurant Recommendation]':
            response = self.restaurant_recommendation_agent.ask_for_inputs()
        elif instruction_name == '[INSTRUCTION: Deliver Restaurant Recommendation]':
            response = self.restaurant_recommendation_agent.generate_recommendation(query)
        else:
            response = 'Sorry, I am not yet capable of performing this task or instruction. Can I help you with anything else?'

        if '`ASSISTANT`:' in response:
            response = response.replace('`ASSISTANT`:', '')
        if 'http://www.flavourflix.com' in response:
            response = response.replace('http://www.flavourflix.com', 'https://flavourflixx.wixsite.com/flavour-flix')
        return response


    def initialize(self, files):
        """Initializes the main agent (Filomena) by initializing all sub-agents.
        Additionally, it first greets the user.
        Parameters:
            - files (list): A list of file paths to load the Question-Answer agent.
        Returns:
            - None
        """

        self.question_agent.initialize_qa(files=files)
        self.greet()


    def generate_response(self, query):
        """Generates the response to the user's question based on
        the correct instruction.
        Parameters:
            - query (str): The question to be answered.
        Returns:
            - response (str): Filomena's answer to the user's question.
        """
        if len((self.model_messages)) <= 5:
            self.messages.append({"role": "user", "content": query})
            self.model_messages.append({"role": "user", "content": query})

            response = self.perform_instruction(query, self.model_messages)

            self.model_messages.append({"role": "assistant", "content": response})
            self.messages.append({"role": "assistant", "content": response})
            return response
        else:
            self.model_messages = reduce_memory(self.model_messages)
            return self.generate_response(query)
    
    def reset(self):
        self.messages = []
        self.model_messages = []
    
