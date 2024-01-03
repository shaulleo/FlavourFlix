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
from openai import OpenAI
from prompt_templates import *



class GPT_Helper:
    def __init__(self,
        OPENAI_API_KEY: str,
        system_behavior: str="",
        model="gpt-3.5-turbo",
    ):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.messages = []
        self.model = model

        if system_behavior:
            self.messages.append({
                "role": "system",
                "content": system_behavior
            })

    # [i] get completion from the model             
    def get_completion(self, prompt, temperature=0.3):

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
    


query_helper =  GPT_Helper(OPENAI_API_KEY=local_settings.OPENAI_API_KEY, system_behavior=prompt_templates['Query Helper System'])


def prep_question(query, chatbot_message):
    prompt = f"""
            The User Message is:{query}
            The ChatBot Message is:{chatbot_message}
            """

    query_formatted = query_helper.get_completion(prompt)
    return query_formatted



class Filomena():
    def __init__(self, ):
        self.llm = ChatOpenAI(temperature=0.3, api_key=local_settings.OPENAI_API_KEY)
        self.memory = ConversationBufferMemory(memory_key="chat_history",  input_key="question")
        self.prompt = PromptTemplate(
            input_variables=["chat_history", "question", "context"], 
            template= prompt_templates['Filomena Template'])
        self.agent_chain = load_qa_chain(self.llm, chain_type="stuff", memory=self.memory, prompt=self.prompt)
        self.messages = []

    def load_documents(self, file_paths, type='pdf'):
        docs = []

        # if type == 'pdf':
        for file_path in file_paths:
                loader = PyPDFLoader(file_path)
                docs.extend(loader.load())

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500,chunk_overlap=200)
        splits = text_splitter.split_documents(docs)

        embeddings = OpenAIEmbeddings()
        vectordb = FAISS.from_documents(splits, embeddings)
        self.vectordb = vectordb

    def generate_response(self, query, identified=False):
        
        self.messages.append({"role": "user", "content": query})

        if not identified:
            try:
                query = prep_question(query, self.messages[-2]['content'])
            except:
                query = query

        response = self.agent_chain(
                    {"input_documents": self.vectordb.max_marginal_relevance_search(query, k=3),
                        "question": f'{query}',},
                    return_only_outputs=True)

        self.messages.append({"role": "assistant","content": response['output_text']})

        return response['output_text']
    
    def reset(self):
        self.messages = []

        
    
    