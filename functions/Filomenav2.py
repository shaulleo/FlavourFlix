from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.memory import ConversationBufferMemory
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from prompts_list import *
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from functions.utils import *

def get_identification_and_user():
    if ('authentication_status' in st.session_state) and (st.session_state['authentication_status'] == True) and ('username' in st.session_state):
        username = st.session_state['username']
        client_data = pd.read_csv('data/clientData.csv')
        if username in client_data['username'].values:
            first_name = client_data[client_data['username'] == username]['first_name'].values[0]
        else:
            first_name = 'Not Provided'
        return f'Username: {username} | First Name: {first_name}'
    else:
        return f'No Identification Provided'
    


identification_vars = get_identification_and_user()

template = """
TASK:
You are Filomena, a virtual assistant specialized in recommending restaurants for FlavourFlix users. \
Your role involves understanding user preferences through conversation and suggesting restaurants that match their tastes and requirements,\
as well as answer any question provided by the user.
Your responses should be friendly, casual, yet professional. 

Consider the instruction type at the beginning of the Human Message between square brackets. 
Depending on the instruction, you should respond as described in the INSTRUCTIONS. 


INSTRUCTIONS:
[Instruction: Identification]
Greet the user by their username or first name, if it exists (is different from "No Identification Provided"). \
Otherwise, greet the user as "Fellow Foodie". 
Introduce yourself and the FlavourFlix service.
Ask the user what they feel like eating today. This question sets the direction for the conversation.
""" + identification_vars + """

[Instruction: Question]
Answer the user's question based on the provided context and chat history.

Also consider in the final answer the chat history, the context, and the Human question.
Context:
{context} 
Chat History:
{chat_history}
Human: 
{question}
Chatbot:
"""

class Filomena():
    def __init__(self, ):
        self.llm = ChatOpenAI(temperature=0.7, api_key=local_settings.OPENAI_API_KEY)
        self.memory = ConversationBufferMemory(memory_key="chat_history",  input_key="question")
        self.prompt = PromptTemplate(
            input_variables=["chat_history", "question", "context"], 
            template=template)
        self.agent_chain = load_qa_chain(self.llm, chain_type="stuff", memory=self.memory, prompt=self.prompt)
        self.messages = []
        

    def load_documents(self, file_paths, type='pdf'):
        docs = []
        if type == 'pdf':
            for file_path in file_paths:
                    loader = PyPDFLoader(file_path)
                    docs.extend(loader.load())
            else:
                raise NotImplementedError
            
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500,chunk_overlap=200)
        splits = text_splitter.split_documents(docs)

        embeddings = OpenAIEmbeddings()
        vectordb = FAISS.from_documents(splits, embeddings)
        self.vectordb = vectordb

    def prep_response(self, query):
        #PREP QUERY WITH IDENTIFIERS 
        pass

    def get_completion(self, query):
        self.messages.append({"role": "user", "content": query})

        response = self.agent_chain(
                    {"input_documents": self.vectordb.similarity_search(query, k=1),
                        "question": f'{prep_response(query)}',},
                    return_only_outputs=True)

        self.messages.append({"role": "assistant","content": response['output_text']})

        return response['output_text']

        
    
    



# prompt = PromptTemplate(
#     input_variables=["chat_history", "question", "context"], 
#     template=template)


# memory = ConversationBufferMemory(memory_key="chat_history",  input_key="question") 

# agent_chain = load_qa_chain(llm, chain_type="stuff", memory=memory, prompt=prompt)

st.title("FlavourFlix Restaurant Assistant - Filomena")


