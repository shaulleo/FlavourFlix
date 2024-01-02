import os
#import utils
from functions.utils import *
import streamlit as st
from functions.chat_bot import *
from prompts_list import *
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.memory import ConversationBufferMemory
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.callbacks.base import BaseCallbackHandler

st.set_page_config(page_title="ChatPDF", page_icon="📄")
st.header('Chat with your documents')
st.write('Has access to custom documents and can respond to user queries by referring to the content within those documents')
st.write('[![view source code ](https://img.shields.io/badge/view_source_code-gray?logo=github)](https://github.com/shashankdeshpande/langchain-chatbot/blob/master/pages/4_%F0%9F%93%84_chat_with_your_documents.py)')


if 'messages' not in st.session_state:
    st.session_state.messages = []

class StreamHandler(BaseCallbackHandler):
    
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs):
        self.text += token
        self.container.markdown(self.text)


def display_msg(msg, author):
    """Method to display message on the UI

    Args:
        msg (str): message to display
        author (str): author of the message -user/assistant
    """
    st.session_state.messages.append({"role": author, "content": msg})
    st.chat_message(author).write(msg)


class Filomena:
    def __init__(self, system_behavior: str="", use_proprietary_data: bool=True):
        self.openai_model = "gpt-3.5-turbo"
        self.use_proprietary_data = use_proprietary_data
        self.messages = []
        if system_behavior:
            self.messages.append({
                "role": "system",
                "content": system_behavior
            })

    def setup_qa_chain(self, file_paths: list = None,):

        if self.use_proprietary_data:
            # Load documents
            docs = []
            for file_path in file_paths:
                loader = PyPDFLoader(file_path)
                docs.extend(loader.load())
            
            # Split documents
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500,chunk_overlap=200)
            splits = text_splitter.split_documents(docs)

            # Create embeddings and store in vectordb
            embeddings = OpenAIEmbeddings()
            vectordb = FAISS.from_documents(splits, embeddings)

            # Define retriever
            retriever = vectordb.as_retriever(
                search_type='mmr',
                search_kwargs={'k':2, 'fetch_k':4}
            )

            # Setup memory for contextual conversation        
            memory = ConversationBufferMemory(
                memory_key= 'chat_history',
                return_messages=True
            )

            # Setup LLM and QA chain
            llm = ChatOpenAI(model_name=self.openai_model, temperature=0, streaming=True, api_key=local_settings.OPENAI_API_KEY)
            qa_chain = ConversationalRetrievalChain.from_llm(llm, retriever=retriever, memory=memory, verbose=True)
            return qa_chain
        else:
            llm = ChatOpenAI(model_name=self.openai_model, temperature=0, streaming=True, api_key=local_settings.OPENAI_API_KEY)
            qa_chain = ConversationalRetrievalChain.from_llm(llm, verbose=True)
            return qa_chain

    

    def main(self, files=['data\CP-23Group4 Project Proposal.pdf', 'data\Food Personalities.pdf']):
            user_query = st.chat_input(placeholder="Ask me anything!")

            if files and user_query:
                qa_chain = self.setup_qa_chain(files)

                display_msg(user_query, 'user')

                with st.chat_message("assistant"):
                    st_cb = StreamHandler(st.empty())
                    response = qa_chain.run(user_query, callbacks=[st_cb])
                    st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    obj = Filomena(system_behavior=prompts_list[0]['prompt'])
    obj.main()