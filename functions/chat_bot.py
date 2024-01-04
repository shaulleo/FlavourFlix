from functions.filomena_prompts import *
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
from functions.utils import *
from openai import OpenAI
from langdetect import detect
from functions.location import *
from functions.preprocessement import *
from langchain.agents import tool
from langchain.agents import load_tools, initialize_agent
from langchain.agents import AgentType



#  ----------------------------- AGENT TOOLS ----------------------------- #

@tool
def get_restaurant_info(restaurant_name):
    """Gathers all the restaurant information from the FlavourFlix restaurant database, based on the name of the restaurant."""
    restaurant_data = pd.read_csv('data\preprocessed_restaurant_data.csv')
    restaurant_data = restaurant_data[restaurant_data['name'] == restaurant_name]
    result = f"""Name: {restaurant_data["name"].values[0]} \n /
    Cuisine Type: {restaurant_data["cuisine"].values[0]} \n /
    Average Price: {restaurant_data["averagePrice"].values[0]} \n /
    Location: {restaurant_data["location"].values[0]} \n /
    Restaurant Style: {restaurant_data["style"].values[0]} \n /
    Restaurant Schedule: {restaurant_data["schedule"].values[0]}"""
    return result


@tool
def get_recommendation(nationality=None, city=None, travel_car=None,  favourite_food=None,  restaurant_style=None,
                       cuisine_type=None, lunch_hour=None, dinner_hour=None,
                       normal_price_range=None):
    """Recommends restaurants based on the user's preferences and requirements."""
    restaurant_data = pd.read_csv('data/preprocessed_restaurant_data.csv')
    filtered_data = restaurant_data.copy()

    conditions = []

    #Location filters such that the restaurant is near the user and the place the user wants to go
    if city:
        city_match = get_data_match(restaurant_data, city, 'city')
        filtered_data = filtered_data[filtered_data['city'] == city_match]
        latitude, longitude = find_coordinates(city_match)
        if latitude is not None and longitude is not None:
            desired_location = Location(latitude, longitude)
            filtered_data = nearYou(desired_location, filtered_data)
            if travel_car:
                filtered_data['minutes_away'] = filtered_data.apply(lambda row: desired_location.getDirections(row['latitude'], row['longitude'], ['driving'])['driving'].minutes, axis=1)
                filtered_data = filtered_data[filtered_data['minutes_away'] <= 35]
            else:
                filtered_data['minutes_away'] = filtered_data.apply(lambda row: desired_location.getDirections(row['latitude'], row['longitude'], ['walking'])['walking'].minutes, axis=1)
                filtered_data = filtered_data[filtered_data['minutes_away'] <= 59]

    #Time filters such that the restaurant is open at the time the user wants to go
    if lunch_hour:
        filtered_data = filter_schedule(filtered_data, dinner_hour, lunch_hour)
    if dinner_hour:
        filtered_data = filter_schedule(filtered_data, dinner_hour, lunch_hour)
    
    #Additional filters
    if nationality and len(filtered_data) != 0:
        nationality_match = get_data_match(restaurant_data, nationality, 'cuisine')
        conditions.append(restaurant_data['cuisine'] == nationality_match)
    
    if restaurant_style:
        restaurant_style_match = get_data_match(restaurant_data, restaurant_style, 'style')
        conditions.append(restaurant_data['style'] == restaurant_style_match)
    
    if cuisine_type:
        cuisine_type_match = get_data_match(restaurant_data, cuisine_type, 'cuisine')
        conditions.append(restaurant_data['cuisine'] == cuisine_type_match)

    if normal_price_range:
        conditions.append(restaurant_data['averagePrice'] <= normal_price_range+4)

    if favourite_food:
        if detect(favourite_food) == 'en':
            conditions.append(restaurant_data['menu_en'].str.contains(favourite_food))
        else:
            conditions.append(restaurant_data['menu_pre_proc'].str.contains(favourite_food))
    

    # Combine conditions with logical OR
    if conditions and len(filtered_data) != 0:
        filtered_data = restaurant_data[pd.concat(conditions, axis=1).any(axis=1)]
    else:
        filtered_data = restaurant_data 

    # Ranking - sort by ratings or other criteria
    restaurant_data = restaurant_data.sort_values(by='ratingValue', ascending=False)

    # Return top recommendations
    return restaurant_data.head(5) 


# ----------------------------- AGENTS ----------------------------- #


class GPT_Helper:
    def __init__(self,
        OPENAI_API_KEY: str,
        system_behavior: str="",
        model="gpt-4",
        #model = "gpt-3.5-turbo"
        # model = "gpt-4-0613"
    ):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.messages = []
        self.model = model

        if system_behavior:
            self.messages.append({
                "role": "system",
                "content": system_behavior
            })

           
    def get_completion(self, prompt, temperature=0.0):
        self.messages = []
        self.messages.append({"role": "user", "content": prompt})
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            temperature=temperature,
        )
        self.messages.append(
            {
                "role": "assistant",
                "content": completion.choices[0].message.content}
        )
        return completion.choices[0].message.content
    

    def get_instruction(self, query, chat_history):
        prompt = """TASK: Your job is to assign an Instruction Identifier based on the user input (query)  \
                        and a chat history. The Instruction Identifiers and their descriptions are:  """ + str(instructions) + f"""OUTPUT:
    You will return the answer in the following format:
    [Instruction: Instruction Identifier] | query
    USER QUERY: {query}
    CHAT HISTORY: {chat_history}""" 

        query_formatted = self.get_completion(prompt)
        if query not in query_formatted:
            query_formatted = f'{query_formatted} | {query}'
        return query_formatted




class QuestionAnsweringBot():
    def __init__(self, ):
        self.llm = ChatOpenAI(temperature=0, api_key=local_settings.OPENAI_API_KEY)
        self.memory = ConversationBufferMemory(memory_key="chat_history",  input_key="question")
        self.prompt = PromptTemplate(
            input_variables=["chat_history", "question", "context"], template= instructions['[INSTRUCTION: Question]']['instruction description'])
        self.agent_chain = load_qa_chain(self.llm, chain_type="stuff", memory=self.memory, prompt=self.prompt)
        self.messages = []
    
    def load_documents(self, files):
        docs = []
        for file_path in files:
                loader = PyPDFLoader(file_path)
                docs.extend(loader.load())
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500,chunk_overlap=200)
        splits = text_splitter.split_documents(docs)
        embeddings = OpenAIEmbeddings()
        vectordb = FAISS.from_documents(splits, embeddings)
        self.vectordb = vectordb

    def initialize_qa(self, files):
        self.load_documents(files)

    def prepare_question(self, query):
        question_preparer = GPT_Helper(OPENAI_API_KEY=local_settings.OPENAI_API_KEY, 
                                       system_behavior = prompt_templates['Preparing Questions']['question_answer'])  
        query = f"""Task: Refine the 'Original prompt' to ensure it is clear, relevant. Start by making the prompt concise and clear, rephrasing any vague 
                or complex sentences. Then, identify the core question or remove unnecessary details to improve relevance.
                Original prompt': {query} 
                Output: 'Refined prompt' """
        query_prepared = question_preparer.get_completion(query)
        return query_prepared

    def generate_response(self, query):

        query_prepared = self.prepare_question(query)
        response = self.agent_chain(
            {
                "input_documents": self.vectordb.similarity_search(query_prepared, k=1),
                "question": f'{query_prepared}',
            },
            return_only_outputs=True,)
        
        return response['output_text']




class RestaurantDescriptionBot():
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0.3, api_key=local_settings.OPENAI_API_KEY, model='gpt-3.5-turbo')
        self.agent= initialize_agent( [get_restaurant_info],
            self.llm,
            agent= AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            handle_parsing_errors=True,
            verbose = False)
        
    def prepare_question(self, query):
        restaurant_data = pd.read_csv('data\preprocessed_restaurant_data.csv')
        question_preparer = GPT_Helper(OPENAI_API_KEY=local_settings.OPENAI_API_KEY, 
                                       system_behavior = prompt_templates['Preparing Questions']['restaurant_description'])  
        query = f"""Task: Obtain the restaurant name from the 'Original prompt'.
                Original prompt': {query}
                Output: 'Restaurant Name'
                """
        restaurant_name = question_preparer.get_completion(query)
        restaurant_name = get_data_match(restaurant_data, restaurant_name, 'name')
        query_prepared = f"""Tell me about the restaurant '{restaurant_name}.'"""
        return query_prepared
        
        
    def generate_response(self, query):
        query_prepared = self.prepare_question(query)
        response = self.agent(query_prepared)
        return response['output']




# ---------------------------- FILOMENA ----------------------------#
    
personality_finder = QuestionAnsweringBot()
personality_finder.initialize_qa(files=[''])
personality_description = personality_finder.generate_response("What are FlavourFlix' personality types? Describe them.")


class Filomena():
    def __init__(self, ):
        self.core_messages = []
        self.core_piece = GPT_Helper(OPENAI_API_KEY=local_settings.OPENAI_API_KEY, system_behavior = prompt_templates['Instruction Identification'])
        self.llm = ChatOpenAI(temperature=0, api_key=local_settings.OPENAI_API_KEY)
        self.messages = []
        self.question_agent = QuestionAnsweringBot()
        self.restaurant_descriptor_agent = RestaurantDescriptionBot()

    def greet(self):
        greeter = GPT_Helper(OPENAI_API_KEY=local_settings.OPENAI_API_KEY, system_behavior = instructions['[INSTRUCTION: Identification]']['instruction description'])
        
        response = greeter.get_completion(f""" INSTRUCTION: Greet the user by their username or first name, if it exists (is different from "No Identification Provided"). \
                                        Otherwise, greet the user as "Fellow Foodie". Introduce yourself as Filomena - FlavourFlix' virtual assistance. 
                                        \Ask the user what they need your help with. """ + identification_vars + """OUTPUT: 'Greeting' """)
        self.messages.extend(greeter.messages[-1:])
        return response

    def perform_instruction(self, query, chat_history):
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
        elif instruction_name == '[INSTRUCTION: What is my personality]':
            if ('personality' in st.session_state and st.session_state['personality'] != None):
                response = f"""You are a {st.session_state['personality']}."""
            else:
                personality_finder = GPT_Helper(OPENAI_API_KEY=local_settings.OPENAI_API_KEY, system_behavior = prompt_templates['Personality Finder'])
                personality_finder.get_completion(f"""INSTRUCTION: Consider the variable 'personality' and its possible values. \ 
                                                  If the value is different from 'Not Available', state that the user is a 'PERSONALITY' and explain the 
                                                  personality in question based on 'PERSONALITY DESCRIPTION'. \
                                                  Otherwise, state that you do not yet have access to the user's personality and that they\
                                                   should take the personality questionnaire available in the app. 
                                                  'PERSONALITY': {personality_type}
                                                    'PERSONALITY DESCRIPTION': {personality_description} 
                                                """ )
            
        else:
            response = 'Sorry, I am not yet capable of performing this task or instruction. Can I help you with anything else?'
        return response


    def initialize(self, files):
        self.question_agent.initialize_qa(files=files)
        self.greet()


    def generate_response(self, query):
        self.messages.append({"role": "user", "content": query})
        response = self.perform_instruction(query, self.messages)
        self.messages.append({"role": "assistant", "content": response})

        return response
    
    def reset(self):
        self.messages = []