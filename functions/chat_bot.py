from prompt_templates import *
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
import spacy
from langchain.agents import tool
from sklearn.metrics.pairwise import cosine_similarity 
from langchain.agents import load_tools, initialize_agent
from langchain.agents import AgentType

# !python -m spacy download en_core_web_md


# ----------------------------- PROMPT TEMPLATES ----------------------------- # (vai para outro folder)


question_answer_template = """
TASK:
You are Filomena, a virtual assistant specialized in recommending restaurants for FlavourFlix users. \
Your role involves answering any question provided by the user about FlavourFlix and all of its functionalities, as well as 
help the user navigate the platform by answering any doubt. \
Your responses should be friendly, casual, yet professional. 

INSTRUCTION:
You will receive a chat history between the ChatBot and the user, and a final query from the user. \
Your job is to answer the user's question based on the provided context, the user question, and the chat history. \

Context:
{context} 
Chat History:
{chat_history}
User: 
{question}
Chatbot:
"""



instructions2 = {
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
                    "The Adventurer", "Fine Dining Connoiser", "Comfort Food Lover", "Low Cost Foodie" and "Conscious Eater" are not restaurant names."""}
                                        }


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



prompt_templates2 = {'Instructions': instructions2,
                     'Instruction Identification': instruction_identifier, 
                     'Preparing Questions': {'question_answer': prepare_question_qa_template, 
                                             'restaurant_description': prepare_restaurant_question_template}}


#  ----------------------------- AGENT TOOLS AND OTHER FUNCTIONS ----------------------------- #

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


def get_data_match(data, word, col_to_match):
    nlp = spacy.load("en_core_web_md")

    word_embedding = nlp(word).vector
    similarities = {}
    for token in list(data[col_to_match].unique()):
        token_embedding = nlp(token).vector
        similarities[token] = cosine_similarity([word_embedding], [token_embedding])[0][0]

    return max(similarities, key=similarities.get)

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
                        and a chat history. The Instruction Identifiers and their descriptions are:  """ + str(instructions2) + f"""OUTPUT:
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
            input_variables=["chat_history", "question", "context"], template= instructions2['[INSTRUCTION: Question]']['instruction description'])
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
                                       system_behavior = prompt_templates2['Preparing Questions']['question_answer'])  
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
                                       system_behavior = prompt_templates2['Preparing Questions']['restaurant_description'])  
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

class Filomena():
    def __init__(self, ):
        self.core_messages = []
        self.core_piece = GPT_Helper(OPENAI_API_KEY=local_settings.OPENAI_API_KEY, system_behavior = prompt_templates2['Instruction Identification'])
        self.llm = ChatOpenAI(temperature=0, api_key=local_settings.OPENAI_API_KEY)
        self.messages = []
        self.question_agent = QuestionAnsweringBot()
        self.restaurant_descriptor_agent = RestaurantDescriptionBot()

    def greet(self):
        greeter = GPT_Helper(OPENAI_API_KEY=local_settings.OPENAI_API_KEY, system_behavior = instructions2['[INSTRUCTION: Identification]']['instruction description'])
        
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