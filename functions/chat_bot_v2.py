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


#  ----------------------------- AGENT TOOLS ----------------------------- #

@tool
def get_restaurant_info(restaurant_name: str):
    """Gathers all the restaurant information from the FlavourFlix restaurant 
    database, based on the name of the restaurant.
    Parameters:
        - restaurant_name (str): The name of the restaurant exactly as 
        it appears in the data.
    Returns:
        - result (str): A string with all the information 
        about the restaurant.
    """
    restaurant_data = pd.read_csv('data/preprocessed_restaurant_data.csv')
    restaurant_data = restaurant_data[restaurant_data['name'] == restaurant_name]
    result = f"""Name: {restaurant_data["name"].values[0]} \n /
    Cuisine Type: {restaurant_data["cuisine"].values[0]} \n /
    Average Price: {restaurant_data["averagePrice"].values[0]} \n /
    Location: {restaurant_data["location"].values[0]} \n /
    Restaurant Style: {restaurant_data["style"].values[0]} \n /
    Restaurant Schedule: {restaurant_data["schedule"].values[0]}"""
    return result

# ----------------------------- AGENTS ----------------------------- #


class GPT_Helper:
    def __init__(self,
        OPENAI_API_KEY: str,
        system_behavior: str="",
        model: str="gpt-3.5-turbo"):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.messages = []
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
        self.llm = ChatOpenAI(temperature=0, api_key=local_settings.OPENAI_API_KEY)
        self.memory = ConversationBufferMemory(memory_key="chat_history",  input_key="question")
        self.prompt = PromptTemplate(
            input_variables=["chat_history", "question", "context"], template= qa_bot_prompts['qa_answerer'])
        self.agent_chain = load_qa_chain(self.llm, chain_type="stuff", memory=self.memory, prompt=self.prompt)
        self.messages = []
    
    def load_documents(self, files: list):
        """Prepares and loads the documents to be used by the 
        agent in a Vector Database.
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
        documents within the Vector Database.
        Parameters:
            - query (str): The question to be answered.
        Returns:
            - response (str): The answer to the user's question.
        """

        query_prepared = self.prepare_question(query)
        response = self.agent_chain(
            {
                "input_documents": self.vectordb.similarity_search(query_prepared, k=1),
                "question": f'{query_prepared}',
            }, return_only_outputs=True,)
        
        return response['output_text']

# ----------------------------- Filomena ----------------------------- #

class Filomena():
    def __init__(self):
        self.core_piece = GPT_Helper(OPENAI_API_KEY=local_settings.OPENAI_API_KEY, 
                                     system_behavior = instruction_identifier['system_configuration'])
        self.llm = ChatOpenAI(temperature=0, 
                              api_key=local_settings.OPENAI_API_KEY)
        self.messages = []
        self.question_agent = QuestionAnsweringBot()
        # self.restaurant_descriptor_agent = RestaurantDescriptionBot()
        # self.restaurant_recommendation_agent = RestaurantRecommendationBot()

    def greet(self):
        greeter = GPT_Helper(OPENAI_API_KEY=local_settings.OPENAI_API_KEY, system_behavior = greeter_prompts['system_configuration'])
        
        response = greeter.get_completion(greeter_prompts['task'])
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
          