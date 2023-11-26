from functions.streamlitfunc import *
from functions.utils import *
import time
import streamlit as st
from functions.chat_bot import  ChatBot
from streamlit_extras.switch_page_button import switch_page 

#st.set_page_config(page_title='Restaurant', page_icon="ext_images\page_icon.png", layout="wide", initial_sidebar_state="collapsed")
                                                                                
def initialize() -> None:
    """
    Initialize the app
    """
    st.title("Ask Filomena 🍲")
    st.write("Ask me anything about portuguese food and restaurants and I'll do my best to answer you! 🇵🇹")
    st.write("Note that the answers are not always 100% accurate, but I'm learning!")

    if "chatbot" not in st.session_state:
        #st.session_state.chatbot = ChatBotStatic()
        model = GPTWrapper(local_settings.OPENAI_API_KEY)
        #model = GPTWrapper('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')
        st.session_state.chatbot = ChatBot(model_manager = model)



def display_history_messages():
    """
    Display chat messages from history on app rerun.
    """
    # Display chat messages from history on app rerun
    for message in st.session_state.chatbot.memory:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])



def display_user_msg(message: str):
    """
    Display user message in chat message container.
    """
    st.session_state.chatbot.memory.append(
        {"role": "user", "content": message}
    )

    with st.chat_message("user", avatar="😎"):
        st.markdown(message)


                                                                         

def display_assistant_msg(message: str):
    """
    Display assistant message
    """
    with st.chat_message("assistant", avatar="👩🏽‍🍳"):
        message_placeholder = st.empty()

        # Simulate stream of response with milliseconds delay
        full_response = ""
        for chunk in message.split():
            full_response += chunk + " "
            time.sleep(0.05)

            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)

        st.session_state.chatbot.memory.append(
            {"role": "assistant", "content": full_response}
        )


if __name__ == "__main__":

    if ('authentication_status' in st.session_state) and (st.session_state['authentication_status'] == True) and ('username' in st.session_state) and ('email' in st.session_state):
        pages_logged_in()
        header_image = "ext_images/logo.jpeg"  
        st.image(header_image, width=400)
        initialize()

        # [i] Display History #
        display_history_messages()

        if prompt := st.chat_input("Type your request..."):

            # [*] Request & Response #
            display_user_msg(message=prompt)
            assistant_response = st.session_state.chatbot.generate_response(
                message=prompt
            )
            display_assistant_msg(message=assistant_response)

    else:
        pages_logged_off()
        st.error('Ups! Something went wrong. Please try login again.', icon='🚨')
        st.session_state['authentication_status'] = False
        st.write('You need to be logged in to access this feature.')
        with st.spinner('Redirecting you to the Login page...'):
            time.sleep(3)
        switch_page('log in')
    # [i] Sidebar #
    # with st.sidebar:
    #     st.write(st.session_state.chatbot.memory)